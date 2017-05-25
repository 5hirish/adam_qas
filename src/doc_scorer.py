import gensim
import re
from collections import Counter, OrderedDict
from pprint import pprint


def query2vec(query, dictionary):
    """
    with open('corpus/stop_words.txt', 'r', newline='') as stp_fp:
        stop_list = (stp_fp.read()).lower().split("\n")
    texts = [word for word in query.lower().split() if word not in stop_list]
    """

    corpus = dictionary.doc2bow(query)
    print("Q:")
    print(corpus)

    return corpus


def doc2vec(documents):
    with open('corpus/stop_words.txt', 'r', newline='') as stp_fp:
        stop_list = (stp_fp.read()).lower().split("\n")
    texts = [[word for word in doc.lower().split() if word not in stop_list]for doc in documents]
    frequency = Counter()
    for sent in texts:
        for token in sent:
            frequency[token] += 1

    texts = [[token for token in snipp if frequency[token] > 1]for snipp in texts]
    print(texts)

    dictionary = gensim.corpora.Dictionary(texts)
    print(dictionary)
    print(dictionary.token2id)

    corpus = [dictionary.doc2bow(snipp) for snipp in texts]
    print("C:")
    print(corpus)

    return corpus, dictionary


def transform_vec(corpus, query_corpus):
    tfidf = gensim.models.TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]
    query_tfidf = tfidf[query_corpus]

    for doc in corpus_tfidf:
        print("C:", doc)
    for doc in query_tfidf:
        print("Q:", doc)

    return corpus_tfidf, query_tfidf


def similariy(corpus_tfidf, query_tfidf):
    index = gensim.similarities.SparseMatrixSimilarity(corpus_tfidf, num_features=100000)

    simi = index[query_tfidf]

    simi_sorted = sorted(enumerate(simi), key=lambda item: -item[1])
    print("Rank:")
    pprint(simi_sorted)
    return simi_sorted


def pre_process_doc(list_docs):

    # (\\n)+
    # (=+[a-zA-Z0-9\s]+=+([a-zA-Z0-9\s]+=+)*)

    regex_newline = re.compile(r'(\n)+')
    regex_apostrophe = re.compile(r'(\')')
    regex_or = re.compile(r'(?<=[A-Za-z.]\s)+/(?=\s+[A-Za-z])')
    regex_sections = re.compile(r'(=+[a-zA-Z0-9\s]+=+([a-zA-Z0-9\s]+=+)*)')

    for doc in range(len(list_docs)):
        snip = list_docs[doc]
        snip = regex_newline.sub("", snip)
        snip = regex_apostrophe.sub(" ", snip)
        snip = regex_or.sub("or", snip)
        snip = regex_sections.sub("", snip)

        list_docs[doc] = snip

    with open('corpus/know_corp.txt', 'w') as fp:
        for op_doc in list_docs:
            fp.write(str(op_doc) + "\n")


def score_docs(documents, keywords):

    keywords = [keywords[feat].lower() for feat in range(0, len(keywords) - 1)]
    print(keywords)
    list_docs = list(documents.values())

    pre_process_doc(list_docs)

    corpus, dictionary = doc2vec(list_docs)
    query_corpus = query2vec(keywords, dictionary)

    corpus_tfidf, query_tfidf = transform_vec(corpus, query_corpus)

    simi_sorted = similariy(corpus_tfidf, query_tfidf)

    return simi_sorted


keywords_ip = ['species', 'Great White shark', 'are']

with open('corpus/know_corp_raw.txt', 'r') as fp:
    documents_ordered = fp.read().split("\n")
    del documents_ordered[len(documents_ordered) - 1]

    print(len(documents_ordered))

score_docs(documents_ordered, keywords_ip)
