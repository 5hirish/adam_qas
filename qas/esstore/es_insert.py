from elasticsearch import Elasticsearch
from qas.esstore.es_connect import ElasticSearchConn


class ElasticSearchInsert:
    es = ElasticSearchConn()
    es_conn = es.get_db_connection()
