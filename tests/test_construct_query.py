import spacy
import json
from unittest import TestCase

from qas.constants import EN_MODEL_MD
from qas.sqlitestore.sqlt_connect import SqLiteManager
from qas.query_const import construct_query

"""
Created by felix on 11/3/18 at 10:57 PM
"""


class TestConstructQuery(TestCase):

    def test_construct_query(self):
        sql_man = SqLiteManager()
        en_nlp_l = spacy.load(EN_MODEL_MD)

        # result = sql_man.get_random_questions(3)
        result = sql_man.get_questions_between(5, 7)

        for row in result:
            qid = row[0]
            with self.subTest(qid):
                question = row[1]
                question_type = row[2]
                question_feat = json.loads(row[3])

                if question_feat is not None:

                    en_doc = en_nlp_l(u'' + question)

                    query = construct_query(question_feat, en_doc)
                    print("{0}){1} :\nQuery: {2}".format(qid, question, repr(query)))
                    js_query = json.dumps(repr(query))
                    sql_man.update_search_query(qid, js_query)
                    assert query is not None
        # sql_man.close_db()
