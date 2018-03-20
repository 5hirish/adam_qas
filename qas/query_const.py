import logging

from qas.model.query_container import QueryContainer
'''
The Query is constructed just to show relationship amongst different features in the feature set.
A conjunction is a part of speech that is used to connect words, phrases, clauses, or sentences. 
'''

"""
Refer http://universaldependencies.org/u/dep/ for dependency labels.
More in-depth at https://nlp.stanford.edu/software/dependencies_manual.pdf
"""

logger = logging.getLogger(__name__)


def get_detail(sentence):
    logger.debug("Word\tLemma\tTag\tEntity\tDependency\tHead")
    for token in sentence:
        logger.debug("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(
                     token.text, token.lemma_, token.tag_, token.ent_type_, token.dep_, token.head))


def get_conjuncts(token):

    """
    A conjunct is the relation between two elements connected by a coordinating conjunction, such as and, or, etc.
     We treat conjunctions asymmetrically: The head of the relation is the first conjunct and all the other conjuncts
      depend on it via the conj relation.

    Coordinating Conjunction: and, or, but, yet, so, nor, for.
    Correlative Conjunctions: either...or, whether...or, not only...but also
    """

    parent = token.head
    conj = [parent.text]

    for child in parent.children:
        if child.dep_ == "conj":
            conj.append(child.text)

    logger.debug("Conjuncting: {0}".format(conj))
    return conj


def get_query(sentence, feature_list):

    """
    This function sequentially adds the query components to the structured query.
    """

    query_container = QueryContainer()
    query_container.add_features(feature_list)

    conjunct_list = []
    neg_list = []
    mark_list = []

    for token in sentence:

        # cc: A cc is the relation between a conjunct and a preceding coordinating conjunction.
        if token.dep_ == "cc":
            logger.debug("Conjunction: `{0}` at {1}".format(token.text, token.i))
            conjunct_list.append(get_conjuncts(token))
            conjunct_list.append(token.text)
            query_container.add_coordinating_conjunct(token.text)

        # neg: The negation modifier is the relation between a negation word and the word it modifies.
        if token.dep_ == "neg":
            if token.i > token.head.i:
                neg_list.append([token.text, token.head.text])
                logger.debug("Negation: `{0}` at `{1}`".format(token.text, token.head.text))
            else:
                neg_list.append([token.head.text, token.text])
                logger.debug("Negation: `{0}` at `{1}`".format(token.text, token.head.text))

        # mark: A marker is the word introducing a finite clause subordinate to another clause.
        if token.dep_ == "mark":
            if token.i > token.head.i:
                mark_list.append([token.text, token.head.text])
                logger.debug("Mark: `{0}` at `{1}`".format(token.text, token.head.text))
            else:
                mark_list.append([token.head.text, token.text])
                logger.debug("Mark: `{0}` at `{1}`".format(token.text, token.head.text))

    query_container.add_conjunctions(conjunct_list)
    query_container.add_negations(neg_list)
    query_container.add_markers(mark_list)

    return query_container


def construct_query(features_list, en_doc):
    query_constructed_obj = []

    for sentence in en_doc.sents:
        query_constructed_obj.append(get_query(sentence, features_list))

    return query_constructed_obj


if __name__ == "__main__":

    import spacy
    from constants import EN_MODEL_MD

    logging.basicConfig(level=logging.DEBUG)
    question = "What are Cushman or Wakefield known for ?"
    features = ['Cushman', 'known', 'Wakefield', 'are']

    en_nlp = spacy.load(EN_MODEL_MD)
    en_doc = en_nlp(u'' + question)

    query = []

    for sent in en_doc.sents:
        get_detail(sent)
        query.append(get_query(sent, features))
        logger.info("Query: {0}".format(repr(query)))
