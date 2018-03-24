from datetime import datetime
import logging

from qas.esstore.es_connect import ElasticSearchConn
from qas.esstore.es_config import __index_name__, __doc_type__, __wiki_pageid__, __wiki_revision__, __wiki_title__, \
    __wiki_content__, __wiki_updated_date__, __wiki_raw__
from qas.model.query_container import QueryContainer
from qas.model.es_document import ElasticSearchDocument

logger = logging.getLogger(__name__)


def resolve_operator(conj_op):
    if conj_op == "and":
        return "and"
    elif conj_op == "or":
        return "or"


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
                "source": "ctx._source." + __wiki_content__ + " = params." + __wiki_content__,
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

    def search_wiki_article(self, search_query):

        """
        Refer:  https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html [6.X]
                https://www.elastic.co/guide/en/elasticsearch/guide/current/full-text-search.html      [2.X]
        """

        """
        The match query is of type boolean.
        The operator flag can be set to `or` or `and` to control the boolean clauses (defaults to or). 
        Bool Query: [must, filter, should]
        The term query looks for the exact term in the field’s inverted index — it doesn’t know anything about the field’s analyzer. 
        
        The match query supports multi-terms synonym expansion with the synonym_graph token filter. 
        When this filter is used, the parser creates a phrase query for each multi-terms synonyms.
        """

        search_res = []

        for query in search_query:
            query_cont = QueryContainer(query)
            if isinstance(query_cont, QueryContainer):
                features = query_cont.get_features()
                conjunct = query_cont.get_conjunctions()
                negations = query_cont.get_negations()
                markers = query_cont.get_markers()

                must_match = []
                should_match = []
                must_not_match = []

                if conjunct is not None and len(conjunct) > 0:
                    for i in range(len(conjunct)):
                        if type(conjunct[i]) is list:
                            features = [feat for feat in features if feat not in conjunct[i]]
                            if i < len(conjunct) - 1:
                                conj_op = conjunct[i + 1]
                                es_operator = resolve_operator(conj_op)
                                must_match_query = {
                                    "match": {
                                        __wiki_content__: {
                                            "query": " ".join(conjunct[i]),
                                            "operator": es_operator
                                        }
                                    }
                                }
                                must_match.append(must_match_query)

                # FIXME: No support for negations with conjunctions

                if negations is not None and len(negations) > 0:
                    for i in range(len(negations)):
                        if type(negations[i]) is list:
                            features = [feat for feat in features if feat not in negations[i]]
                            if i < len(conjunct) - 1:
                                conj_op = conjunct[i + 1]
                                es_operator = resolve_operator(conj_op)
                                must_not_match_term = {
                                    __wiki_content__: {
                                        "query": " ".join(conjunct[i]),
                                        "operator": es_operator
                                    }
                                }
                                must_not_match.append(must_not_match_term)

                if features is not None and len(features) > 0:
                    # must_match_query = {"terms": {__wiki_content__: features}}
                    # must_match.append(must_match_query)
                    # for feat in features:
                    #     must_match_term = {"term": {__wiki_content__: feat}}
                    #     must_match.append(must_match_term)
                    must_match_query = {
                        "match": {
                            __wiki_content__: {
                                "query": " ".join(features)
                            }
                        }
                    }
                    must_match.append(must_match_query)

                # wiki_features = {"must": must_match_term}

                search_body = {
                    "query": {
                        "bool": {
                            "must": must_match,
                            "should": should_match,
                            "must_not": must_not_match,
                        }
                    }
                }

                logger.debug(search_body)

                es_result = self.es_conn.search(index=__index_name__, doc_type=__doc_type__, body=search_body)
                if es_result['hits']['hits'] is not None:
                    es_result_hits = es_result['hits']['hits']
                    for result in es_result_hits:
                        article_id = result['_id']
                        article_score = result['_score']
                        article_source = result['_source']
                        es_document = ElasticSearchDocument(article_id, article_source, article_score)
                        search_res.append(es_document)

            else:
                raise ValueError("Incorrect Query Type")

        return search_res


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    # mquery = list([[['Cushman', 'known', 'Wakefield', 'are'], [['Cushman', 'Wakefield'], 'or'], [], []]])
    mquery = list([[['Albert', 'Einstein', 'birth'], [], [], []]])

    es = ElasticSearchOperate()
    res_all = es.search_wiki_article(mquery)
    for res in res_all:
        print(res.get_wiki_title())
