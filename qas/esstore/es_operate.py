import logging
import warnings
from datetime import datetime

from qas.esstore.es_config import __index_name__, __wiki_revision__, __wiki_title__, \
    __wiki_content__, __wiki_content_info__, __wiki_content_table__, __wiki_updated_date__, __wiki_raw__
from qas.esstore.es_connect import ElasticSearchConn
from qas.model.es_document import ElasticSearchDocument
from qas.model.query_container import QueryContainer

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
        warnings.warn("Deprecated: This will insert the document without any checks.", DeprecationWarning)
        wiki_body = {
            __wiki_revision__: revid,
            __wiki_title__: title,
            __wiki_raw__: raw,
            __wiki_updated_date__: datetime.now()
        }
        res = self.es_conn.index(index=__index_name__, body=wiki_body, id=pageid)
        logger.debug("Article Inserted:{0}".format(res['result']))
        return res['result'] == 'created' or res['result'] == 'updated'

    def upsert_wiki_article(self, pageid, revid, title, raw):
        warnings.warn("Deprecated: This will upsert the complete document in any case, instead of upserting only if"
                       "revision id changes.", DeprecationWarning)

        wiki_body = {
            "doc": {
                __wiki_revision__: revid,
                __wiki_title__: title,
                __wiki_raw__: raw,
                __wiki_updated_date__: datetime.now()
            },
            "doc_as_upsert": True
        }
        res = self.es_conn.update(index=__index_name__, body=wiki_body, id=pageid)
        logger.debug("Article Upserted:{0}".format(res['result']))
        return res['result'] == 'created' or res['result'] == 'updated'

    def upsert_wiki_article_if_updated(self, pageid, revid, title, raw):

        """
        Refer: https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html
        If the document does not already exist, the contents of the upsert element will be inserted as a new document.
        If the document does exist, then the script will be executed instead
        """

        wiki_body = {
            "script": {
                "source": "if (ctx._source."+__wiki_revision__+" < params.new_revision) "
                                                               "{ctx._source = params.new_article } "
                                                               "else {ctx.op = 'none' }",
                "lang": "painless",
                "params": {
                    "new_revision": revid,
                    "new_article": {
                        __wiki_revision__: revid,
                        __wiki_title__: title,
                        __wiki_raw__: raw,
                        __wiki_updated_date__: datetime.now()
                    }
                }
            },
            "upsert": {
                __wiki_revision__: revid,
                __wiki_title__: title,
                __wiki_raw__: raw,
                __wiki_updated_date__: datetime.now()
            }
        }
        res = self.es_conn.update(index=__index_name__, body=wiki_body, id=pageid)
        logger.debug("Article Upserted:{0}".format(res['result']))
        return res['result'] == 'created' or res['result'] == 'updated' or res['result'] == 'noop'

    def update_wiki_article(self, pagid, content=None, content_info=None, content_table=None):
        wiki_body = None

        if content is not None:
            wiki_body = {
                "script": {
                    "source": "ctx._source." + __wiki_content__ + " = params." + __wiki_content__,
                    "lang": "painless",
                    "params": {
                        __wiki_content__: content
                    }
                }
            }

        elif content_info is not None:
            wiki_body = {
                "script": {
                    "source": "ctx._source." + __wiki_content_info__ + " = params." + __wiki_content_info__,
                    "lang": "painless",
                    "params": {
                        __wiki_content_info__: content_info
                    }
                }
            }

        elif content_table is not None:
            wiki_body = {
                "script": {
                    "source": "ctx._source." + __wiki_content_table__ + " = params." + __wiki_content_table__,
                    "lang": "painless",
                    "params": {
                        __wiki_content_table__: content_table
                    }
                }
            }

        if wiki_body is not None:
            res = self.es_conn.update(index=__index_name__, id=pagid, body=wiki_body)
            logger.debug("Article Updated:{0}".format(res['result']))
            return res['result'] == 'updated'
        else:
            return None

    def get_wiki_article(self, pageid):
        res = self.es_conn.get(index=__index_name__, id=pageid)
        logger.debug("Article Fetched:{0}".format(res['found']))
        if res['found']:
            return res['_source']
        else:
            return None

    def delete_wiki_article(self, pageid):
        res = self.es_conn.delete(index=__index_name__, id=pageid)
        logger.debug("Article Deleted:{0}".format(res['result']))
        return res['result'] == 'deleted'

    def extract_info_from_article(self, features, conjunct, conj, index):
        if isinstance(conj, list):
            features = [feat for feat in features if feat not in conj]
            if index < len(conjunct) - 1:
                conj_op = conjunct[index + 1]
        return conj_op

    # def extract_info_here(self, negations, features, conj_op, es_operator, must_nut_match):
    #     if (negations is not None and len(negations) > 0:
    #         for index, negate in enumerate(negations):
    #             if isinstance(negate, list):
    #                 features = [feat for feat in features if feat not in negate]
    #                 if index < len(negations - 1)
    #                     conj_op = negations[index + 1]
    #                 es_operator = resolve_operator(conj_op)
    #     return negations

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
        
        The multi_match query builds on the match query to allow multi-field queries. We can sepcify the fields to be queried.
        The way the multi_match query is executed internally depends on the type parameter.
        The most_fields finds documents which match any field and combines the _score from each field.
        """

        search_res = []

        for query in search_query:
            if not isinstance(query, QueryContainer):
                query_cont = QueryContainer(query)
            else:
                query_cont = query
            if isinstance(query_cont, QueryContainer):
                features = query_cont.get_features()
                conjunct = query_cont.get_conjunctions()
                negations = query_cont.get_negations()
                # markers = query_cont.get_markers()

                must_match = []
                should_match = []
                must_not_match = []

                if conjunct is not None and len(conjunct) > 0:
                    for index, conj in enumerate(conjunct):
                        conj_op = self.extract_info_from_article(features, conjunct, conj, index)
                        es_operator = resolve_operator(conj_op)
                        must_match_query = {
                            "multi_match": {
                                "query": " ".join(conj),
                                "operator": es_operator,
                                "type": "most_fields",
                                "fields": [__wiki_content__, __wiki_content_info__, __wiki_content_table__]
                            }
                        }
                        must_match.append(must_match_query)
                # FIXME: No support for negations with conjunctions

                if negations is not None and len(negations) > 0:
                    for index, negate in enumerate(negations):
                        conj_op = self.extract_info_from_article(features, negations, negate, index)
                        es_operator = resolve_operator(conj_op)
                        must_not_match_term = {
                            "multi_match": {
                                "query": " ".join(negations[index]),
                                "operator": es_operator,
                                "type": "most_fields",
                                "fields": [__wiki_content__, __wiki_content_info__, __wiki_content_table__]
                            }
                        }
                        must_not_match.append(must_not_match_term)

                if features is not None and len(features) > 0:
                    must_match_query = {
                        "multi_match": {
                            "query": " ".join(features),
                            "type": "most_fields",
                            "fields": [__wiki_content__, __wiki_content_info__, __wiki_content_table__]
                        }
                    }
                    must_match.append(must_match_query)

                search_body = self.build_body(must_match, must_not_match, should_match)

                logger.debug(search_body)

                es_result = self.es_conn.search(index=__index_name__, body=search_body)
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

    def build_body(self, must_match, must_not_match, should_match):
        search_body = {
            "query": {
                "bool": {
                    "must": must_match,
                    "should": should_match,
                    "must_not": must_not_match,
                }
            }
        }
        return search_body


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    mquery = list([[['Albert', 'Einstein', 'birth'], [], [], []]])

    es = ElasticSearchOperate()
    res_all = es.search_wiki_article(mquery)
    for lres in res_all:
        print(lres.get_wiki_title())
