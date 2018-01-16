from elasticsearch import Elasticsearch

"""
Meta Class for managing elasticsearch db connection. It also serves as an singleton
"""


class ElasticSearchMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ElasticSearchMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ElasticSearchConn(metaclass=ElasticSearchMeta):
    __hostname__ = 'localhost'
    __port__ = 9200
    __es_conn__ = None

    def __init__(self):
        self.__es_conn__ = Elasticsearch([{'host': self.__hostname__, 'port': self.__port__}])

    def get_db_connection(self):
        return self.__es_conn__
