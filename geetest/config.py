# coding:utf-8

import logging
import os
import re


def get_env(key, default):
    return os.environ.get(key, default)


REG_MONGODB = re.compile(r'mongodb://(?:(?P<username>.+?):(?P<password>.+?)@)?'
                         r'(?P<host>.+?)(?::(?P<port>\d+?))?/(?P<db>.+)')
BASE_PATH = os.path.dirname(__file__)


def get_mongodb_setting(mongodb_uri):
    setting = REG_MONGODB.search(mongodb_uri).groupdict()
    setting.update({"port": int(setting.get("port") or 27017)})
    return setting


class DevConfig(object):
    # flask basic config
    SECRET_KEY = b'\xa28\xb4rN\x90[\r\x8f\xb8J\x15\xa3e\x02z\xc5\xe8dzNv+\x1b'

    # mongodb config
    MONGODB_URI = get_env('MONGODB_URI', "mongodb://127.0.0.1:27017/spider_db")
    MONGODB_SETTINGS = get_mongodb_setting(mongodb_uri=MONGODB_URI)

    # log config
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s[%(lineno)s]: %(message)s"
    LOG_PATH = get_env("LOG_PATH", os.path.join(BASE_PATH, "logs"))
    LOG_LEVEL = logging.DEBUG

    DEBUG = True


class DemoConfig(DevConfig):
    DEBUG = False
    LOG_PATH = get_env("LOG_PATH", os.path.join(BASE_PATH, "/var/log/postman"))


class ProdConfig(DevConfig):
    DEBUG = False
    LOG_PATH = get_env("LOG_PATH", os.path.join(BASE_PATH, "/var/log/postman"))
