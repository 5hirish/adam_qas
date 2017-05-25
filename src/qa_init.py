import spacy
from enchant import Dict
from autocorrect import spell
from re import compile
from time import time

from src.qclassifier import classify_question
from src.feature_extractor import extract_features
from src.query_const import construct_query
from src.fetch_wiki import fetch_wiki
from src.doc_scorer import rank_docs


def spell_check(input_question):

    pattern = "\W"
    prog = compile(pattern)

    input_question_word_list = input_question.split()
    en_dict = Dict("en_US")
    for word_index in range(len(input_question_word_list)):
        if not en_dict.check(input_question_word_list[word_index]) and prog.match(input_question_word_list[word_index]) is None:
            correct_word = spell(input_question_word_list[word_index])
            input_question_word_list[word_index] = correct_word
    return " ".join(input_question_word_list)

# input_question = input("Q:>")
input_question = "How many species of the Great White shark are there ?"
# input_question_c = spell_check(input_question)
input_question_c = input_question
print("Question:", input_question_c)

start_time = time()

en_nlp = spacy.load('en_core_web_md')

en_doc = en_nlp(u'' + input_question_c)

question_class = classify_question(en_doc)
print("Class:", question_class)

question_keywords = extract_features(question_class, en_doc)
print("Question Features:", question_keywords)

question_query = construct_query(question_keywords, en_doc)
print("Question Query:", question_query)

print("Fetching Knowledge source...")
wiki_pages = fetch_wiki(question_keywords, number_of_search=3)
print("Pages Fetched:", len(wiki_pages))

ranked_wiki_docs = rank_docs(question_keywords)
print("Ranked Pages:", ranked_wiki_docs)

end_time = time()
print("Total time :", end_time - start_time)
