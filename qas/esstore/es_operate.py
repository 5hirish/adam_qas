from datetime import datetime
import logging
from qas.esstore.es_connect import ElasticSearchConn
from qas.esstore.es_config import __index_name__, __doc_type__, __wiki_pageid__, __wiki_revision__, __wiki_title__, \
    __wiki_content__, __wiki_updated_date__, __wiki_raw__

logger = logging.getLogger(__name__)


class ElasticSearchOperate:
    es_conn = None

    def __init__(self):
        es = ElasticSearchConn()
        self.es_conn = es.get_db_connection()

    def insert_wiki_article(self, pageid, revid, title, raw):
        wiki_body = {
            __wiki_revision__: revid,
            __wiki_title__: title,
            __wiki_raw__: raw,
            __wiki_updated_date__: datetime.now()
        }
        res = self.es_conn.index(index=__index_name__, doc_type=__doc_type__, body=wiki_body, id=pageid)
        logger.debug("Article Inserted:{0}".format(res['result']))
        return res['result'] == 'created' or res['result'] == 'updated'

    def upsert_wiki_article(self, pageid, revid, title, raw):
        wiki_body = {
            "doc": {
                __wiki_revision__: revid,
                __wiki_title__: title,
                __wiki_raw__: raw,
                __wiki_updated_date__: datetime.now()
            },
            "doc_as_upsert": True
        }
        res = self.es_conn.update(index=__index_name__, doc_type=__doc_type__, body=wiki_body, id=pageid)
        logger.debug("Article Inserted:{0}".format(res['result']))
        return res['result'] == 'created' or res['result'] == 'updated'

    # def update_wiki_article(self, pageid, content):
    #     wiki_body = {
    #         "script": {
    #             "source": "ctx._source."+__wiki_content__+"='"+content+"'",
    #             "lang": "painless"
    #         },
    #         "query": {
    #             "match": {
    #                 __wiki_pageid__: pageid
    #             }
    #         }
    #     }
    #     res = self.es_conn.update_by_query(index=__index_name__, doc_type=__doc_type__, body=wiki_body)
    #     return res['updated']

    def update_wiki_article(self, pagid, content):
        wiki_body = {
            "script": {
                "source": "ctx._source."+__wiki_content__+" = params."+__wiki_content__,
                "lang": "painless",
                "params": {
                    __wiki_content__: content
                }
             }
        }
        res = self.es_conn.update(index=__index_name__, doc_type=__doc_type__, id=pagid, body=wiki_body)
        logger.debug("Article Updated:{0}".format(res['result']))
        return res['result'] == 'updated'

    def get_wiki_article(self, pageid):
        res = self.es_conn.get(index=__index_name__, doc_type=__doc_type__, id=pageid)
        logger.debug("Article Fetched:{0}".format(res['found']))
        if res['found']:
            return res['_source']
        else:
            return None

    def delete_wiki_article(self, pageid):
        res = self.es_conn.delete(index=__index_name__, doc_type=__doc_type__, id=pageid)
        logger.debug("Article Deleted:{0}".format(res['result']))
        return res['result'] == 'deleted'


