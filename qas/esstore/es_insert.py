from elasticsearch import Elasticsearch
from datetime import datetime
from qas.esstore.es_connect import ElasticSearchConn
from qas.esstore.es_config import __index_name__, __doc_type__, __wiki_pageid__, __wiki_revision__, __wiki_title__, \
    __wiki_content__, __wiki_updated_date__, __wiki_raw__


class ElasticSearchInsert:
    es = ElasticSearchConn()
    es_conn = es.get_db_connection()

    def insert_wiki_article(self, pageid, revid, title, raw):
        wiki_body = {
            __wiki_pageid__: pageid,
            __wiki_revision__: revid,
            __wiki_title__: title,
            __wiki_raw__: raw,
            __wiki_updated_date__: datetime.now()
        }
        res = self.es_conn.index(index=__index_name__, doc_type=__doc_type__, body=wiki_body)
        return res['created']

    def update_wiki_article(self, pageid, content):
        wiki_body = {
            "script": {
                "source": "ctx._source."+__wiki_content__+"='"+content+"'",
                "lang": "painless"
            },
            "query": {
                "match": {
                    __wiki_pageid__: pageid
                }
            }
        }
        res = self.es_conn.update_by_query(index=__index_name__, doc_type=__doc_type__, body=wiki_body)
        return res['updated']
