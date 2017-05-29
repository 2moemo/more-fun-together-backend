import traceback
from xml.etree import ElementTree as elementTree
from base.design import Singleton


class Config(Singleton):
  environment = None
  debug = None
  netTimeOut = 0
  netNumOfConnection = 0

  dbHost = None
  dbPort = None
  dbName = None
  dbUser = None
  dbPassword = None
  dbNumOfConnection = 0

  redisHost = None
  redisPort = None
  redisUser = None
  redisPassword = None
  redisNumOfConnectionMinimum = 0
  redisNumOfConnectionMaximum = 0

  def __init__(self):
    try:
      with open('config.xml', 'r') as file:
        configXML = elementTree.fromstring(''.join(file.readlines()))

        # basic
        Config.environment = configXML.find('environment').text
        Config.debug = configXML.find('debug').text == 'true'

        # net
        Config.netTimeOut = int(configXML.find('net').find('timeOut').text)
        Config.netNumOfConnection = int(configXML.find('net').find('numOfConnection').text)

        # db
        Config.dbHost = configXML.find('db').find(Config.environment).find('host').text
        Config.dbPort = int(configXML.find('db').find(Config.environment).find('port').text)
        Config.dbName = configXML.find('db').find(Config.environment).find('dbName').text
        Config.dbUser = configXML.find('db').find(Config.environment).find('user').text
        Config.dbPassword = configXML.find('db').find(Config.environment).find('password').text
        Config.dbNumOfConnection = int(configXML.find('db').find(Config.environment).find('numOfConnection').text)

        # redis
        Config.redisHost = configXML.find('redis').find(Config.environment).find('host').text
        Config.redisPort = int(configXML.find('redis').find(Config.environment).find('port').text)
        Config.redisUser = configXML.find('redis').find(Config.environment).find('user').text
        Config.redisPassword = configXML.find('redis').find(Config.environment).find('password').text
        redisNumOfConnectionMinimum = int(
          configXML.find('redis').find(Config.environment).find('numOfConnectionMinimum').text)
        redisNumOfConnectionMaximum = int(
          configXML.find('redis').find(Config.environment).find('numOfConnectionMaximum').text)

    except:
      print(traceback.format_exc())
