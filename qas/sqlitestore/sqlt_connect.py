import os
import sys
import logging
import sqlite3

from qas.corpus.data import QA_TEST_DATA
from constants import CORPUS_DIR

"""
Created by felix on 8/3/18 at 1:40 AM
"""

logger = logging.getLogger(__name__)


class SqLiteMeta:
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SqLiteMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SqLiteManager(metaclass=SqLiteMeta):

    __test_db__ = CORPUS_DIR + "/" + QA_TEST_DATA
    __sqlt_conn__ = None

    def __init__(self, db_name=__test_db__):
        self.__sqlt_conn__ = sqlite3.connect(db_name)

    def get_db_cursor(self):
        return self.__sqlt_conn__.cursor()

    def commit_db(self):
        self.__sqlt_conn__.commit()

    def close_db_(self):
        self.__sqlt_conn__.close()


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) > 1:
        arguments = sys.argv

    else:
        raise ValueError('Missing Arguments')