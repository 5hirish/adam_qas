from fuzzywuzzy import fuzz
from pprint import pprint
import spacy


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

    keywords = [keywords[feat].lower() for feat in range(0, len(keywords))]
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


def fuzzy_match(sentences, keywords_query):
    simi_sorted = []
    for sent_id in range(len(sentences)):
        white_space = ' '
        keywords_query_str = white_space.join(keywords_query)
        ratio = fuzz.token_set_ratio(keywords_query_str, sentences[sent_id].text.lower())
        simi_tuple = (ratio, sent_id)
        simi_sorted.append(simi_tuple)
    simi_sorted = sorted(simi_sorted, key=lambda x: -x[0])
    return simi_sorted


def get_candidate_answers(question_query, ranked_wiki_docs, en_nlp):

    keywords_query = pre_query(question_query)
    # print(keywords_query)

    document = get_processed_document(ranked_wiki_docs)

    en_doc = en_nlp(u'' + document)

    sentences = list(en_doc.sents)

    simi_sorted = fuzzy_match(sentences, keywords_query)

    if len(simi_sorted) > 10:
        simi_sorted = simi_sorted[0:10]

    candidate_ans = []
    for sent in simi_sorted:
        sent_id = sent[0]
        candidate_ans.append(str(sentences[sent_id]))

    return candidate_ans, keywords_query

question_query = [['color Johnny Cash', 'stage', 'wear'], [], [], []]
wiki_ranks = [(0, 0.2428495), (3, 0.20424521), (2, 0.12708507)]
en_nlp = spacy.load('en_core_web_md')
candidate_answers, keyword_split = get_candidate_answers(question_query, wiki_ranks, en_nlp)
pprint(candidate_answers)