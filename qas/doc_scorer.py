import os
import re
import logging
from collections import Counter

import gensim

from qas.constants import CORPUS_DIR
from esstore.es_operate import ElasticSearchOperate
from esstore.es_config import __wiki_content__

logger = logging.getLogger(__name__)

# Document scoring should be done on elasticsearch and not with this
# search terms [....] where document id is [...or...]


def query2vec(query, dictionary):
    """
    with open('corpus/stop_words.txt', 'r', newline='') as stp_fp:
        stop_list = (stp_fp.read()).lower().split("\n")
    texts = [word for word in query.lower().split() if word not in stop_list]
    """

    corpus = dictionary.doc2bow(query)
    # print("Q:")
    # print(corpus)

    return corpus


def doc2vec(documents):
    with open(os.path.join(CORPUS_DIR, 'stop_words.txt'), 'r', newline='') as stp_fp:
        stop_list = (stp_fp.read()).lower().split("\n")
    texts = [[word for word in doc.lower().split() if word not in stop_list]for doc in documents.values()]
    frequency = Counter()
    for sent in texts:
        for token in sent:
            frequency[token] += 1

    texts = [[token for token in snipp if frequency[token] > 1]for snipp in texts]
    # print(texts)

    dictionary = gensim.corpora.Dictionary(texts)
    # print(dictionary)
    # print(dictionary.token2id)

    corpus = [dictionary.doc2bow(snipp) for snipp in texts]
    # print("C:")
    # print(corpus)

    return corpus, dictionary


def transform_vec(corpus, query_corpus):
    tfidf = gensim.models.TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]
    query_tfidf = tfidf[query_corpus]

    """
    for doc in corpus_tfidf:
        print("C:", doc)
    for doc in query_tfidf:
        print("Q:", doc)
    """

    return corpus_tfidf, query_tfidf


def similariy(corpus_tfidf, query_tfidf):
    index = gensim.similarities.SparseMatrixSimilarity(corpus_tfidf, num_features=100000)

    simi = index[query_tfidf]

    simi_sorted = sorted(enumerate(simi), key=lambda item: -item[1])
    # print("Rank:")
    # pprint(simi_sorted)
    return simi_sorted


def pre_process_doc(list_docs):

    # (\\n)+
    # (=+[a-zA-Z0-9\s]+=+([a-zA-Z0-9\s]+=+)*)

    regex_newline = re.compile(r'(\\n)+')
    regex_references = re.compile(r'== References(.)+')
    regex_apostrophe = re.compile(r"(\\')")
    regex_or = re.compile(r'(?<=[A-Za-z.]\s)+/(?=\s+[A-Za-z])')
    regex_sections = re.compile(r'(=+[a-zA-Z0-9\s]+=+([a-zA-Z0-9\s]+=+)*)')
    regex_whitespace = re.compile(r"(\s)+")

    for doc in list_docs:
        snip = list_docs[doc]
        snip = regex_newline.sub(" ", snip)
        snip = regex_references.sub("", snip)
        snip = regex_apostrophe.sub("'", snip)
        snip = regex_or.sub("or", snip)
        snip = regex_sections.sub("", snip)
        snip = regex_whitespace.sub(" ", snip)

        list_docs[doc] = snip

    with open(os.path.join(CORPUS_DIR, 'know_corp.txt'), 'w') as fp:
        for op_doc in list_docs:
            fp.write(str(op_doc) + "\n")


def combine(sub_keys, keywords_splits, lb, mb, ub):
    whitespace = ' '
    while mb != ub:
        keywords_splits.append(whitespace.join(sub_keys[lb: mb]))
        keywords_splits.append(whitespace.join(sub_keys[mb: ub]))
        mb += 1
    del sub_keys[0]
    if len(sub_keys) > 2:
        combine(sub_keys, keywords_splits, 0, 1, len(sub_keys))


def keywords_splitter(keywords, keywords_splits):

    for key in keywords:
        sub_keys = key.split()

        if len(sub_keys) > 2:
            combine(sub_keys, keywords_splits, 0, 1, len(sub_keys))


def score_docs(documents, keywords):

    keywords = [keywords[feat].lower() for feat in range(0, len(keywords) - 1)]
    whitespace = ' '
    keywords_splits = whitespace.join(keywords).split()

    keywords_splitter(keywords, keywords_splits)
    keywords_splits = list(set(keywords_splits + keywords))
    # print(keywords_splits)

    # pre_process_doc(documents)

    corpus, dictionary = doc2vec(documents)
    query_corpus = query2vec(keywords_splits, dictionary)

    corpus_tfidf, query_tfidf = transform_vec(corpus, query_corpus)

    simi_sorted = similariy(corpus_tfidf, query_tfidf)

    if len(simi_sorted) > 3:
        return simi_sorted[0:3]
    return simi_sorted


def rank_docs(keywords, page_ids):

    doc_dictionary = {}

    es_conn = ElasticSearchOperate()
    for page in page_ids:
        doc_data = es_conn.get_wiki_article(page)
        if __wiki_content__ in doc_data:
            doc_dictionary[page] = doc_data[__wiki_content__]

    # with open(os.path.join(CORPUS_DIR, 'know_corp_raw.txt'), 'r') as fp:
    #     documents_raw = fp.read().split("\n")
    #     del documents_raw[len(documents_raw) - 1]
    #
    #     # print(len(documents_raw))
    #     documents = []
    #
    #     for docs in documents_raw:
    #         docs = docs[1:len(docs) - 1]
    #         documents.append(docs)

    ranked_docs = score_docs(doc_dictionary, keywords)

    # pprint(ranked_docs)

    return ranked_docs


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    keywords_ip = ['albert einstein', 'birth']
    page_ids = [736, 18742711, 12738235, 83443, 18978770, 79449]
    rank_docs = rank_docs(keywords_ip, page_ids)
    print(rank_docs)
