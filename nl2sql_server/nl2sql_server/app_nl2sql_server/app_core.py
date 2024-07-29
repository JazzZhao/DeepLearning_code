# -*- coding: utf-8 -*-
import logging
from flask import Flask

from utils import log_file


def creat_app():
    # 将flask的static_folder作为中间结果目录的全局变量
    app = Flask(__name__)
    log_file(logging.INFO)

    return app

app = creat_app()

