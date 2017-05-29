# -*- coding: utf-8 -*-
import traceback
import datetime
from setting.config import Config
import sys


def log(*contents):
  try:
    if not Config.debug:
      return

    recordTime = str(datetime.datetime.now())
    print(
      '\n------------------------------------------------------------------------------------------------------------------------------')
    print('[@ Record time]: %s' % recordTime)
    for seq, content in enumerate(contents):
      # print('%s: %s' % (seq, content))
      print(content)

  except:
    print(traceback.format_exc())
