from configparser import ConfigParser
import os.path


def getConfig() -> ConfigParser:
    '''
    Возвращает объект ConfigParser из которого можно читать параметры.
    '''
    config = ConfigParser()
    config.read(os.path.dirname(__file__) + "/../settings.ini")
    return config


def check():
    pass
