import sys
import logging
import sqlite3

from qas.corpus.data import QA_TEST_DATA
from qas.constants import CORPUS_DIR

"""
Created by felix on 8/3/18 at 1:40 AM
"""

logger = logging.getLogger(__name__)


class SqLiteMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SqLiteMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SqLiteManager(metaclass=SqLiteMeta):

    __test_db__ = CORPUS_DIR + "/" + QA_TEST_DATA
    __sqlt_conn__ = None
    sqlt_cursor = None
    table_name = "wikiqa"

    def __init__(self, db_name=__test_db__):
        self.__sqlt_conn__ = sqlite3.connect(db_name)
        self.create_table()

    def get_db_cursor(self):
        if self.sqlt_cursor is None:
            self.sqlt_cursor = self.__sqlt_conn__.cursor()
        return self.sqlt_cursor

    def commit_db(self):
        self.__sqlt_conn__.commit()

    def close_db(self):
        # Since here the connection is a singleton, closing the db will close the db but will not delete the object.
        self.__sqlt_conn__.close()

    def create_table(self):
        create_query = """CREATE TABLE IF NOT EXISTS """+self.table_name+""" (
            Qid integer PRIMARY KEY,
            Question text,
            Class text,
            Features text,
            Query text,
            Pages text,
            Ranks text,
            Answer text)
        """
        self.get_db_cursor().execute(create_query)
        self.commit_db()

    def insert_many_question(self, question_set):
        insert_many_query = """INSERT INTO """+self.table_name+""" 
            (Question) VALUES (?)"""
        self.get_db_cursor().executemany(insert_many_query, question_set)
        self.commit_db()

    def get_question_count(self):
        count_questions_query = """SELECT COUNT(*) FROM """+self.table_name
        self.get_db_cursor().execute(count_questions_query)
        result = self.get_db_cursor().fetchone()
        return result[0]

    def get_all_questions(self, limit=0):
        if limit > 0:
            fetch_all_question = """SELECT * FROM """+self.table_name+""" LIMIT """+str(limit)
        else:
            fetch_all_question = """SELECT * FROM """+self.table_name
        self.get_db_cursor().execute(fetch_all_question)
        return self.get_db_cursor().fetchall()

    def get_random_questions(self, limit=0):
        if limit > 0:
            fetch_all_question = """SELECT * FROM """+self.table_name+""" ORDER BY RANDOM() LIMIT """+str(limit)
        else:
            fetch_all_question = """SELECT * FROM """+self.table_name+""" ORDER BY RANDOM()"""
        self.get_db_cursor().execute(fetch_all_question)
        return self.get_db_cursor().fetchall()

    def get_questions_between(self, start, end):
        fetch_range_question = """SELECT * FROM """+self.table_name+""" WHERE Qid BETWEEN """+str(start)+""" AND """+str(end)
        self.get_db_cursor().execute(fetch_range_question)
        return self.get_db_cursor().fetchall()

    def update_feature(self, qid, features):
        update_feature = """UPDATE """+self.table_name+""" SET Features = ? WHERE Qid = """+str(qid)
        self.get_db_cursor().execute(update_feature, (features,))
        self.commit_db()

    def update_search_query(self, qid, query):
        update_feature = """UPDATE """+self.table_name+""" SET Query = ? WHERE Qid = """+str(qid)
        self.get_db_cursor().execute(update_feature, (query,))
        self.commit_db()

    def remove_all_data(self):
        delete_all = """DELETE FROM """+self.table_name
        self.get_db_cursor().execute(delete_all)
        self.commit_db()

    def remove_old_results(self):
        update_many_query = """UPDATE """+self.table_name+""" 
            SET Class = ?, Features = ?, Query = ?, Pages = ?, Ranks = ?, Answer = ?
            WHERE (Class IS NOT NULL OR Features IS NOT NULL OR Query IS NOT NULL OR Pages IS NOT NULL
                    OR Ranks IS NOT NULL OR Answer IS NOT NULL)"""
        self.get_db_cursor().execute(update_many_query, (None, None, None, None, None, None))
        self.commit_db()


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) > 1:
        arguments = sys.argv

    else:
        raise ValueError('Missing Arguments')