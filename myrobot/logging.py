# -*- coding:utf-8 -*-

import logging
from logging import FileHandler
from Robot import constant

DEBUG = logging.DEBUG
INFO = logging.INFO
ERROR = logging.ERROR
WARNING = logging.WARNING


def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(INFO)
    file_handler = FileHandler(constant.LOGGING_PATH)
    logger.addHandler(file_handler)
    return logger
