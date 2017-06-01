import gensim
from collections import Counter, OrderedDict
from pprint import pprint


def query2vec(query, dictionary):

    corpus = dictionary.doc2bow(query)

    return corpus


def doc2vec(documents):
    with open('corpus/stop_words.txt', 'r', newline='') as stp_fp:
        stop_list = (stp_fp.read()).lower().split("\n")
    texts = [[word for word in doc.text.lower().split() if word not in stop_list]for doc in documents]

    frequency = Counter()
    for sent in texts:
        for token in sent:
            frequency[token] += 1

    texts = [[token for token in snipp if frequency[token] > 1]for snipp in texts]

    dictionary = gensim.corpora.Dictionary(texts)
    # print(dictionary)
    # print(dictionary.token2id)

    corpus = [dictionary.doc2bow(snipp) for snipp in texts]

    return corpus, dictionary


def transform_vec(corpus, query_corpus):
    lsidf = gensim.models.LsiModel(corpus)

    corpus_lsidf = lsidf[corpus]
    query_lsidf = lsidf[query_corpus]

    return corpus_lsidf, query_lsidf


def similariy(corpus_lsidf, query_lsidf):
    index = gensim.similarities.SparseMatrixSimilarity(corpus_lsidf, num_features=100000)

    simi = index[query_lsidf]

    simi_sorted = sorted(enumerate(simi), key=lambda item: -item[1])
    # print("Rank:")
    # pprint(simi_sorted)
    return simi_sorted


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


def pre_query(question_query):

    keywords = question_query[0]
    keywords_conjunct = question_query[1]

    print(keywords)

    keywords = [keywords[feat].lower() for feat in range(0, len(keywords) - 1)]
    whitespace = ' '
    keywords_splits = whitespace.join(keywords).split()

    keywords_splitter(keywords, keywords_splits)
    keywords_splits = list(set(keywords_splits + keywords))

    return keywords_splits


def get_processed_document(ranked_wiki_docs):

    with open('corpus/know_corp.txt', 'r') as fp:
        documents = fp.read().split("\n")
        del documents[len(documents) - 1]

        processed_documents = ""

        for rank_tuple in ranked_wiki_docs:
            processed_documents += documents[rank_tuple[0]]

    return processed_documents


def get_candidate_answers(question_query, ranked_wiki_docs, en_nlp):

    keywords_query = pre_query(question_query)
    # print(keywords_query)

    document = get_processed_document(ranked_wiki_docs)

    en_doc = en_nlp(u'' + document)

    sentences = list(en_doc.sents)

    corpus, dictionary = doc2vec(sentences)

    query_corpus = query2vec(keywords_query, dictionary)

    corpus_lsidf, query_lsidf = transform_vec(corpus, query_corpus)

    simi_sorted = similariy(corpus_lsidf, query_lsidf)

    simi_sorted = simi_sorted[0:5]

    result_ans = ""
    for sent in simi_sorted:
        sent_id = sent[0]
        result_ans += str(sentences[sent_id])

    return result_ans
