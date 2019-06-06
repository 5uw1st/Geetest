# coding:utf-8

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_mongoengine import MongoEngine
from geetest.config import ProdConfig

mongodb = MongoEngine()


def get_logger(name, app, level=None):
    app_config = app.config
    log_format, log_path, log_level = app_config["LOG_FORMAT"], app_config["LOG_PATH"], app_config["LOG_LEVEL"]
    logger = logging.getLogger(name)
    if len(logger.handlers) == 2:
        return logger
    logger_file = os.path.join(log_path, "{0}.log".format(name))

    logging_format = logging.Formatter(log_format)

    logger_level = level or log_level

    file_handler = TimedRotatingFileHandler(logger_file, when="D", backupCount=30)
    file_handler.setLevel(logger_level)
    file_handler.setFormatter(logging_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)
    console_handler.setFormatter(logging_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logger_level)
    return logger


def create_app(config=None, logger_name=None):
    config = config or os.getenv('FLASK_CONFIG') or 'geetest.config.DevConfig'
    app = Flask(__name__)

    app.config.from_object(config)

    # init logger
    if logger_name is not None:
        with app.app_context():
            app.logger = get_logger(name=logger_name, app=app)

    # init mongodb
    mongodb.init_app(app)

    return app
