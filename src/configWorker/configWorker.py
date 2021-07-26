from configparser import ConfigParser
import os.path


def get_config() -> ConfigParser:
    config = ConfigParser()
    config.read(os.path.dirname(__file__) + "/../settings.ini")
    return config


def check():
    pass
