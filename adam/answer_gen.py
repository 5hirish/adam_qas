import gensim
from collections import Counter, OrderedDict
import spacy
from pprint import pprint


def query2vec(query, dictionary):

    corpus = dictionary.doc2bow(query)

    return corpus


def doc2vec(documents):
    with open('corpus/stop_words.txt', 'r', newline='') as stp_fp:
        stop_list = (stp_fp.read()).lower().split("\n")
    texts = [[word for word in doc.lemma_.split() if word not in stop_list]for doc in documents]

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


def get_candidate_answers(split_keywords, candidate_answer, en_nlp):

    whitespace = ' '

    document = whitespace.join(candidate_answer)

    en_doc = en_nlp(u'' + document)

    sentences = list(en_doc.sents)

    corpus, dictionary = doc2vec(sentences)

    query_corpus = query2vec(split_keywords, dictionary)

    corpus_lsidf, query_lsidf = transform_vec(corpus, query_corpus)

    simi_sorted = similariy(corpus_lsidf, query_lsidf)
    print(simi_sorted)

    if len(simi_sorted) > 5:
        simi_sorted = simi_sorted[0:5]

    result_ans = ""
    for sent in simi_sorted:
        sent_id = sent[0]
        print(sent_id, sentences[sent_id])
        result_ans = result_ans + " " + str(sentences[sent_id])

    return result_ans


en_nlp = spacy.load('en_core_web_md')

keywords = ['color johnny cash', 'cash', 'johnny', 'johnny cash', 'color johnny', 'stage', 'color', 'wear']
document = ['He recorded Johnny Cash Reads.', 'He wore other colors on stage early in his career, but he claimed to like wearing black both on and off stage.', 'Theatre technique Theatre "Johnny Cash and His Woman is an album by American country singer Johnny Cash and features his wife, June Carter Cash.', 'The Johnny Cash Trail features art selected by a committee that included Cindy Cash, a 2-acre (0.81 ha)', "The Johnny Cash Museum, located in one of Cash's properties in Hendersonville until 2006, dubbed the House of Cash, was sold based on Cash's will."]

get_candidate_answers(keywords, document, en_nlp)