import platform
import elasticsearch

from qas.esstore.es_connect import ElasticSearchConn


def get_system_info():
    print("System:", platform.system())
    print("Platform:", platform.version())
    print("Python:", platform.python_version())
    print("Elasticsearch:", str(elasticsearch.__version__))
    print("Elasticsearch Mapping: ", ElasticSearchConn().get_index_mapping())


if __name__ == "__main__":
    get_system_info()