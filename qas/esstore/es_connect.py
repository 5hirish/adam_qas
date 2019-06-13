import logging
import sys

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError as ESConnectionError
from urllib3.exceptions import NewConnectionError

from qas.esstore.es_config import __index_name__, __wiki_title__, __wiki_updated_date__, __wiki_content__, \
    __wiki_content_info__, __wiki_content_table__, __wiki_revision__, __wiki_raw__, __num_shards__, \
    __num_replicas__, __analyzer_en__, __analyzer_adam__, __index_version__

"""
Meta Class for managing elasticsearch db connection. It also serves as an singleton
"""

logger = logging.getLogger(__name__)


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
    es_index_config = None

    def __init__(self):
        es_host = {'host': self.__hostname__, 'port': self.__port__}
        self.__es_conn__ = Elasticsearch(hosts=[es_host])
        self.set_up_index()

    @staticmethod
    def get_index_mapping():
        return {
            "settings": {
                "number_of_shards": __num_shards__,
                "number_of_replicas": __num_replicas__,
                "analysis": {
                    "filter": {
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        },
                        "english_porter2": {
                            "type": "stemmer",
                            "language": "porter2"
                        }
                    },
                    "analyzer": {
                        __analyzer_adam__: {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "english_stop",
                                "english_porter2"
                            ]
                        }
                    }
                },
            },
            "mappings": {
                "_meta": {
                    "version": 2
                },
                "properties": {
                    __wiki_title__: {
                        "type": "text",
                        "analyzer": __analyzer_adam__
                    },
                    __wiki_updated_date__: {
                        "type": "date"
                    },
                    __wiki_raw__: {
                        "type": "object",
                        "enabled": "false"
                    },
                    __wiki_content__: {
                        "type": "text",
                        "analyzer": __analyzer_adam__
                    },
                    __wiki_content_info__: {
                        "type": "text",
                        "analyzer": __analyzer_adam__
                    },
                    __wiki_content_table__: {
                        "type": "text",
                        "analyzer": __analyzer_adam__
                    },
                    __wiki_revision__: {
                        "type": "long"
                    }
                }
            }
        }

    def create_index(self):
        # ignore 400 cause by IndexAlreadyExistsException when creating an index
        self.es_index_config = ElasticSearchConn.get_index_mapping()
        res = self.__es_conn__.indices.create(index=__index_name__, body=self.es_index_config, ignore=400)
        if 'error' in res and res['status'] == 400:
            # NOTE: Illegal argument errors are also being masked here, so test the index creation
            error_type = res['error']['root_cause'][0]['type']
            if error_type == 'resource_already_exists_exception':
                logger.debug("Index already exists")
            else:
                logger.error("Error Occurred in Index creation:{0}".format(res))
                print("\n -- Unable to create Index:"+error_type+"--\n")
                sys.exit(1)
        elif res['acknowledged'] and res['index'] == __index_name__:
            logger.debug("Index Created")
        else:
            logger.error("Index creation failed:{0}".format(res))
            print("\n -- Unable to create Index--\n")
            sys.exit(1)

    def update_index(self, current_version):

        """
        Existing type and field mappings cannot be updated. Changing the mapping would mean invalidating already indexed documents.
        Instead, you should create a new index with the correct mappings and reindex your data into that index.
        """

        updated_mapping = None

        # Migrating from version 1 to version 2
        if current_version == 1 and __index_version__ == 2:
            updated_mapping = {
                "_meta": {
                        "version": __index_version__
                    },
                "properties": {
                    __wiki_content_info__: {
                        "type": "text",
                        "analyzer": __analyzer_en__
                    },
                    __wiki_content_table__: {
                        "type": "text",
                        "analyzer": __analyzer_en__
                    }
                }
            }

        if updated_mapping is not None:
            self.__es_conn__.indices.close(index=__index_name__)
            res = self.__es_conn__.indices.put_mapping(index=__index_name__, body=updated_mapping)
            self.__es_conn__.indices.open(index=__index_name__)

    def set_up_index(self):
        try:
            try:
                try:
                    index_exists = self.__es_conn__.indices.exists(index=__index_name__)
                    if not index_exists:
                        self.create_index()
                    else:
                        res = self.__es_conn__.indices.get_mapping(index=__index_name__)
                        try:
                            current_version = res[__index_name__]['mappings']['_meta']['version']
                            if current_version < __index_version__:
                                self.update_index(current_version)
                            elif current_version is None:
                                logger.error("Old Index Mapping. Manually reindex the index to persist your data.")
                                print("\n -- Old Index Mapping. Manually reindex the index to persist your data.--\n")
                                sys.exit(1)
                        except KeyError:
                            logger.error("Old Index Mapping. Manually reindex the index to persist your data.")
                            print("\n -- Old Index Mapping. Manually reindex the index to persist your data.--\n")
                            sys.exit(1)

                except ESConnectionError as e:
                    logger.error("Elasitcsearch is not installed or its service is not running. {0}".format(e))
                    print("\n -- Elasitcsearch is not installed or its service is not running.--\n", e)
                    sys.exit(1)
            except NewConnectionError:
                pass
        except ConnectionRefusedError:
            pass

    def get_db_connection(self):
        return self.__es_conn__


if __name__ == "__main__":
    es = ElasticSearchConn()
    es_conn = es.get_db_connection()