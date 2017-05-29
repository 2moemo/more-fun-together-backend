# -*- coding: utf-8 -*-

import traceback
# import aioredis
# import redis
from setting.config import Config
from module.printer import log


class Redis:
  pool = None

  def __init__(self):
    try:
      pass
    except:
      log(traceback.format_exc())

  async def execute(self):
    try:
      pass
    except:
      log(traceback.format_exc(s))
