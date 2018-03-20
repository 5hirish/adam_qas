
class QueryContainer:

    """
    This is class is created to help map the query to elasticsearch _search API
    [0] - Features
    [1] - Conjunctions (nested list with the conjunct and coordinating conjunction)
    [2] - Negations
    [3] - Markers
    """

    __constructed_query__ = [None] * 4
    coordinating_conjuncts = []

    def __init__(self, ip_query=None):
        if ip_query is not None and len(ip_query) == 4:
            self.__constructed_query__ = ip_query

    def add_features(self, feature_list):
        self.__constructed_query__[0] = feature_list

    def add_conjunctions(self, conjunction_list):
        self.__constructed_query__[1] = conjunction_list

    def add_coordinating_conjunct(self, c_conjunct):
        self.coordinating_conjuncts.append(c_conjunct)

    def add_negations(self, negation_list):
        self.__constructed_query__[2] = negation_list

    def add_markers(self, marker_list):
        self.__constructed_query__[3] = marker_list

    def get_constructed_qery(self):
        return self.__constructed_query__

    def get_features(self):
        return self.__constructed_query__[0]

    def get_conjunctions(self):
        return self.__constructed_query__[1]

    def get_negations(self):
        return self.__constructed_query__[2]

    def get_markers(self):
        return self.__constructed_query__[3]

    def __repr__(self):
        return "{Features: "+str(self.__constructed_query__[0]) + " ," \
               "Conjunction: "+str(self.__constructed_query__[1]) + " ," \
               "Negations: "+str(self.__constructed_query__[2]) + " ,"\
               "Marker: "+str(self.__constructed_query__[3]) + "}"
