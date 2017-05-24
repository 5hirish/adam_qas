import enchant
import autocorrect
import re
import spacy
import time

from src.qclassifier import classify_question
from src.feature_extractor import extract_features
from src.query_const import construct_query


def spell_check(input_question):

    pattern = "\W"
    prog = re.compile(pattern)

    input_question_word_list = input_question.split()
    en_dict = enchant.Dict("en_US")
    for word_index in range(len(input_question_word_list)):
        if not en_dict.check(input_question_word_list[word_index]) and prog.match(input_question_word_list[word_index]) is None:
            correct_word = autocorrect.spell(input_question_word_list[word_index])
            input_question_word_list[word_index] = correct_word
    return " ".join(input_question_word_list)


input_question = "How many species of the Great White shark are there ?"
# input_question_c = spell_check(input_question)
input_question_c = input_question

start_time = time.time()

en_nlp = spacy.load('en_core_web_md')

en_doc = en_nlp(u'' + input_question_c)

question_class = classify_question(en_doc)
print("Class:", question_class)

question_keywords = extract_features(question_class, en_doc)
print("Question Features:", question_keywords)

question_query = construct_query(question_keywords, en_doc)
print("Question Query:", question_query)

end_time = time.time()
print("Total time :", end_time - start_time)