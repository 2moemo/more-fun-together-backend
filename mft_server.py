import logging

from aiohttp.web import Response
import api_hour
import aiohttp.web
import multidict
import asyncio
import ujson
import json
from setting.config import Config
from module.net import Net
from module.redis import Redis
from service.handler import Handler as serviceHandler
from module.printer import log

logging.basicConfig(level=logging.INFO)  # enable logging for api_hour


class Container(api_hour.Container):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Declare HTTP server
    self.servers['http'] = aiohttp.web.Application(loop=kwargs['loop'])
    self.servers['http'].ah_container = self  # keep a reference in HTTP server to Container
    self.init_http_server()

  # Define HTTP routes
  def init_http_server(self):
    # Basic
    self.servers['http'].router.add_route('*', '/', self.index)
    self.servers['http'].router.add_route('*', '/healthCheck', self.index)

  # A HTTP handler example
  # More documentation: http://aiohttp.readthedocs.org/en/latest/web.html#handler
  async def index(self, request):
    method = request.method
    path = request.path
    requestContentType = request.headers.get('Content-Type')
    accept = request.headers.get('ACCEPT', 'application/json')
    acceptEncoding = request.headers.get('ACCEPT-ENCODING')
    referer = request.headers.get('Referer')

    responseHeader = multidict.MultiDict(
      {
        'Content-Type': accept,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Cookie, Accept,X-PINGOTHER',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Max-Age': '3600',
        'Access-Control-Allow-Credentials': 'true'
      },
    )

    # Check method
    # if method not in ('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'): # Read, Create, Update, Delete,
    if method not in ('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'):  # Read, Create, Update, Delete,
      responseBody = '[%s] is not allowed method' % method
    # Check data type
    elif method != 'GET' and requestContentType not in ('application/json', 'application/xml', 'text/xml'):
      responseBody = '[%s] is not allowed Content-Type' % requestContentType
    # Health check
    elif path == '/healthCheck':
      responseBody = '200'
    # Business logic
    else:
      if method == 'GET':
        parameters = dict(request.GET)
      else:
        body = await request.text()
        requestData = {}
        if body:
          requestData = ujson.loads(body)
        parameters = requestData.get('parameters', {})

        # Print request payload
        log(str(ujson.dumps(parameters)))

      requestDict = {
        'method': method,
        'service': path,
        'parameters': parameters
      }

      # Service response (Business logic)
      serviceResponse = await serviceHandler(serverInstance=self, requestDict=requestDict).execute()

      # response
      responseBody = {
        'response': serviceResponse,
        'request': requestDict
      }
      responseBody = ujson.dumps(responseBody)

    response = Response(text=responseBody,
                        headers=responseHeader)
    return response

  # Container methods
  async def start(self):
    Config.instance()  # Load Configs & create instance
    Net()  # Create communication instance
    Redis()  # Create redis instance

    await super().start()

  async def stop(self):
    # A coroutine called when the Container is stopped
    await super().stop()

  def make_servers(self):
    # This method is used by api_hour command line to bind your HTTP server on socket
    return [self.servers['http'].make_handler(logger=self.worker.log,
                                              keep_alive=self.worker.cfg.keepalive,
                                              access_log=self.worker.log.access_log,
                                              access_log_format=self.worker.cfg.access_log_format)]
