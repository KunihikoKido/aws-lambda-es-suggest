# -*- coding: utf-8 -*-
import os
import logging
from pystache.loader import Loader
BASE_PATH = os.path.dirname(__file__)

DEBUG = False

LOG_LEVEL = logging.INFO

TIMEOUT = 30

loader = Loader(
    search_dirs=(os.path.join(BASE_PATH, 'templates'),),
    file_encoding='utf-8',
    extension='json'
)

QUERY_TEMPLATE = loader.load_name('query')

DEFAULT_SUGGEST_SIZE = 8
MAX_SUGGEST_SIZE = DEFAULT_SUGGEST_SIZE * 2

try:
    from local_settings import *
except ImportError:
    pass
