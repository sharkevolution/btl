#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler

# _current_dir1 = os.getcwd()
_current_dir = os.path.dirname(__file__)
_current_dir += '/mysite'
exm = os.path.normpath(_current_dir)

BASE_DIR = os.path.join(__file__)

connect_str = None
heroku = None

connect_base = "dbname='mylocaldb' user='postgres' host='localhost' password='sitala'"


def update_connect(connect_base):
    global connect_str

    connect_str = connect_base


def update_heroku(heroku_flag):
    global heroku

    heroku = heroku_flag



def main_log():

    global exm

    level = logging.INFO

    mylog =  os.path.join(exm, 'microblog.log')
    file_handler = RotatingFileHandler(mylog, 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    logger = logging.getLogger('info')
    logger.addHandler(file_handler)
    logger.setLevel(level)  # even if not required...

    return logger



access_name = ['Демо', '1 день', '3 дня', '7 дней', '30 дней']
