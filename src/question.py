# This file process the question

# ----------Imports------------

import spacy

# -----------------------------

def print_coarse_pos(token):
    print(token.pos_)

def print_fine_pos(token):
    print(token.tag_)


# -----------------------------


nlp = spacy.en.English()

# question = raw_input("Q:")

question = "Who is Linus Torvalds and where is he now?"

doc = nlp(u""+question)

for token in doc:
    
    print_fine_pos(token)
    print_coarse_pos(token)