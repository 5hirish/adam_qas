# This file process the question

# ----------Imports------------

import time
import spacy
import spacy.parts_of_speech

# -----------------------------


def word_is_in_entity(word):
    return word.ent_type != 0


def dependency_labels_to_root(token):
    '''Walk up the syntactic tree, collecting the arc labels.'''
    dep_labels = []
    while token.head is not token:
        dep_labels.append(token.dep)
        token = token.head
    return dep_labels


def print_coarse_pos(token):
    print(token.pos_)


def print_fine_pos(token):
    print token, ":", token.tag_, "(Lemma:", token.lemma_, ")"


def is_adverb(token):
    return token.pos == spacy.parts_of_speech.ADV


def iter_products(docs):
    for doc in docs:
        for ent in doc.ents:
            if ent.label_ == 'PRODUCT':
                yield ent

# -----------------------------


nlp = spacy.en.English()

question = raw_input("Q:")

start_time = time.time()

# question = "Who is Linus Torvalds and where is he now?"
print "\n\t", question
doc = nlp(u"" + question)

print "\nNamed entities recognition:"

for token in doc.ents:
    print token.orth_, ":", token.label_

print "\nFine Part of Speech Tagging:"
for token in doc:
    print_fine_pos(token)

print "\nSyntactic dependencies:"
for token in doc:
    #print dependency_labels_to_root(token)
    print(token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights])

print "\nNoun Chunks:"
for chunk in doc.noun_chunks:
    print(chunk.label_, chunk.orth_, '<--', chunk.root.head.orth_)


"""print "Coarse POS"
for token in doc:
    print_coarse_pos(token)"""

print("\n--- %s seconds ---" % (time.time() - start_time))
