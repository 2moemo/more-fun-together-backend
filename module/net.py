# -*- coding: utf-8 -*-
import traceback
import asyncio
import aiohttp
from setting.config import Config
from module.printer import trace


class Net():
  connection = None

  def __init__(self, url='', method='GET', headers=None, body=None, params=None):
    try:
      self.url = url
      self.method = method
      self.headers = headers
      self.body = body
      self.params = params
    except:
      trace(traceback.format_exc())

  async def open(self):
    try:
      pass
    except:
      trace(traceback.format_exc())

  async def close(self):
    try:
      pass
    except:
      trace(traceback.format_exc())

  async def execute(self):
    result = ''
    try:
      pass
    except:
      trace(traceback.format_exc())
    return result
