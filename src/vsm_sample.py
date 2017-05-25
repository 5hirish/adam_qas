import gensim
from collections import Counter
from pprint import pprint
from wikipedia import search
import os
"""
Question: How many species of the Great White shark are there ?
Class: ['NUM']
Question Features: ['species', 'Great White shark', 'are']
Question Query: [['species', 'Great White shark', 'are'], [], [], []]
Pages Fetched: 6
Total time : 98.90474677085876
"""


def query2vec(query, dictionary):
    """
    with open('corpus/stop_words.txt', 'r', newline='') as stp_fp:
        stop_list = (stp_fp.read()).lower().split("\n")
    texts = [word for word in query.lower().split() if word not in stop_list]
    """

    corpus = dictionary.doc2bow(query.lower().split())
    print("Q:")
    pprint(corpus)

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
    pprint(texts)

    dictionary = gensim.corpora.Dictionary(texts)
    print(dictionary)
    print(dictionary.token2id)

    corpus = [dictionary.doc2bow(snipp) for snipp in texts]
    print("C:")
    pprint(corpus)

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
    index = gensim.similarities.SparseMatrixSimilarity(corpus_tfidf, num_features=12)
    simi = index[query_tfidf]
    simi_sorted = sorted(enumerate(simi), key=lambda item: -item[1])
    pprint(simi_sorted)
    return simi_sorted


documents = ["Human machine interface for lab abc computer applications",       # 0
             "A survey of user opinion of computer system response time",       # 1
             "The EPS user interface management system",                        # 2
             "System and human system engineering testing of EPS",              # 3
             "Relation of user perceived response time to error measurement",   # 4
             "The generation of random binary unordered trees",                 # 5
             "The intersection graph of paths in trees",                        # 6
             "Graph minors IV Widths of trees and well quasi ordering",         # 7
             "Graph minors A survey"]                                           # 8

query = "Human computer interaction"

corpus, dictionary = doc2vec(documents)
query_corpus = query2vec(query, dictionary)

corpus_tfidf, query_tfidf = transform_vec(corpus, query_corpus)

simi_sorted = similariy(corpus_tfidf, query_tfidf)