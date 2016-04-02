# This file process the question

# ----------Imports------------

import time
import spacy
import spacy.parts_of_speech


# -----------------------------


def word_is_in_entity(word):
    return word.ent_type != 0


def print_coarse_pos(token):
    print(token.pos_)


def print_fine_pos(token):
    print token, ":", token.tag_


def is_adverb(token):
    return token.pos == spacy.parts_of_speech.ADV


def iter_products(docs):
    for doc in docs:
        for ent in doc.ents:
            if ent.label_ == 'PRODUCT':
                yield ent

# -----------------------------


nlp = spacy.en.English()

# question = raw_input("Q:")

start_time = time.time()

question = "Who is Linus Torvalds and where is he now?"

doc = nlp(u"" + question)

print "Names entities recognition:"

for token in doc.ents:
    print token.orth_, ":", token.label_

print "Fine Part Of Speech Tagging:"
for token in doc:
    print_fine_pos(token)

"""print "Coarse POS"
for token in doc:
    print_coarse_pos(token)"""

print("--- %s seconds ---" % (time.time() - start_time))