import traceback
import asyncio
import importlib
from setting.config import Config
from module.printer import log


class Handler:
  def __init__(self, serverInstance=None, requestDict=None):
    try:
      self.serverInstance = serverInstance
      self.requestDict = requestDict
      self.response = {}
    except:
      print(traceback.format_exc())

  @asyncio.coroutine
  def execute(self):
    try:
      service = self.requestDict.get('service', '')
      serviceModulePath = 'service' + service.replace('/', '.')
      importedModule = importlib.import_module(serviceModulePath)

      serviceModuleNames = serviceModulePath.split('.')
      serviceNameTail = serviceModuleNames[len(serviceModuleNames) - 1]
      className = serviceNameTail[0].upper() + serviceNameTail[1:]

      serviceClass = getattr(importedModule, className)

      self.response = yield from serviceClass(self.requestDict).execute()
    except:
      log(traceback.format_exc())

    return self.response
