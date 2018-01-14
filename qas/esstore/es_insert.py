from elasticsearch import Elasticsearch
from qas.esstore.es_connect import __hostname__, __port__


class ElasticSearchInsert:

    es = Elasticsearch([{'host': __hostname__, 'port': __port__}])
