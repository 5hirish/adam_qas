import enchant
import autocorrect
import re


def spell_check(input_question):

    pattern = "\W"
    prog = re.compile(pattern)

    input_question_word_list = input_question.split(" ")
    en_dict = enchant.Dict("en_US")
    for word_index in range(len(input_question_word_list)):
        if not en_dict.check(input_question_word_list[word_index]) and prog.match(input_question_word_list[word_index]) is not None:
            correct_word = autocorrect.spell(input_question_word_list[word_index])
            input_question_word_list[word_index] = correct_word
    return str(input_question_word_list)


input_question = "Why are ya stopin Googling bro, turn the arw up ?"
print(spell_check(input_question))