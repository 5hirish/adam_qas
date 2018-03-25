import spacy
import json
from unittest import TestCase

from qas.constants import EN_MODEL_MD
from qas.sqlitestore.sqlt_connect import SqLiteManager
from qas.feature_extractor import extract_features

"""
Created by felix on 11/3/18 at 7:21 PM
"""


class TestExtractFeatures(TestCase):

    def test_extract_features(self):
        sql_man = SqLiteManager()
        en_nlp_l = spacy.load(EN_MODEL_MD)

        # result = sql_man.get_random_questions(3)
        result = sql_man.get_questions_between(5, 7)

        for row in result:
            qid = row[0]
            with self.subTest(qid):
                question = row[1]
                question_type = row[2]

                en_doc = en_nlp_l(u'' + question)

                features = extract_features(question_type, en_doc, True)
                print("{0}){1} :\nExtracted: {2}".format(qid, question, features))
                js_feat = json.dumps(features)
                sql_man.update_feature(qid, js_feat)
                assert features is not None
        # sql_man.close_db()
