# ----------Imports------------

import spacy

# -----------------------------

nlp = spacy.en.English()

sentence = "When was Linus Torvalds born ?"
#sentence = raw_input("S:")

print("Named Entity Recognition:")

doc = nlp(u""+sentence)

"""
for sent in doc2.sents:                                                         Sentence Segmentation
    print sent
"""

for token in doc.ents:
    print(token.orth_, ":", token.label_)

print("Noun Chunk:")

for chunk in doc.noun_chunks:
    print(chunk.orth_, '<--', chunk.root.head.orth_)

print("Flags")

for token in doc:                                               # Word Segmentation
    # print token.orth_                                    # Original
    print(token.orth_.lower())                              # Lower-case
    # print token.orth_[:3]                                # A length-N substring from the start of the word
    # print token.orth_[2:]                                # A length-N substring from the end of the word.
    print("Alpha:", token.orth_.isalpha())
    print("Digit:", token.orth_.isdigit())
    print("Space:", token.orth_.isspace())
    print("Lemma:", token.lemma_)                           # The base of the word, with no inflectional suffixes
    print("POS:", token.pos_, " (", token.tag_, ")")                              # ADJ, ADP, ADV, AUX, CONJ, DET, INTJ, NOUN, NUM, PART, PRON, PROPN, PUNCT, SCONJ, SYM, VERB, X, EOL, SPACE.
    print("Entity type:", token.ent_type)

    #print "URL", token.orth_.like_url()
    #print "Number", token.orth_.like_num()
    #print "Email", token.orth_.like_email()
    #print "Out of vocabulary", token.orth_.is_oov()"""

example = "The boy with the spotted dog quickly ran after the firetruck."
parsedEx = nlp(u"", example)
# shown as: original token, dependency tag, head word, left dependents, right dependents
for token in parsedEx:
    print(token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights])

