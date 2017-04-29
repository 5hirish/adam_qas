'''

Feature Extractor

Based on Question Type
Feature Extraction

Candidate selection: Here, we extract all possible words, phrases, terms or concepts (depending on the task) that can potentially be keywords.
Properties calculation: For each candidate, we need to calculate properties that indicate that it may be a keyword.
Scoring and selecting keywords: All candidates can be scored by either combining the properties into a formula, or using a machine learning technique to determine probability of a candidate being a keyword

'''

import spacy


def get_detail(sent):
    for token in sent:
        print(token.text, token.lemma_, token.tag_, token.ent_type_, token.dep_)


def get_compound_nouns(token, token_text):

    for child in token.children:
        if child.dep_ == "compound":
            token_text = child.text + " " + token_text
            token_text = get_compound_nouns(child, token_text)

        if child.dep_ == "amod":
            token_text = child.text + " " + token_text
            token_text = get_compound_nouns(child, token_text)

    return token_text


def get_noun_chunk(sent):
    root = ""
    for token in sent:
        if token.tag_ == "NN" or token.tag_ == "NNP" or token.tag_ == "NNPS" or token.tag_ == "NNS":
            if token.dep_ != "compound":
                token_text = get_compound_nouns(token, token.text)
                keywords.append(token_text)

        if token.dep_ == "ROOT":
            root = token.text
    return root


# text = "What team did baseball's St. Louis Browns become ?"
# text = "What contemptible scoundrel stole the cork from my lunch ?"
# text = "What fowl grabs the spotlight after the Chinese Year of the Monkey ?"
# text = "What is an annotated bibliography ?"
text = "What is the origin of the name ' Scarlett ' ?"


en_nlp = spacy.load('en')
en_doc = en_nlp(u'' + text)
keywords = []

for sent in en_doc.sents:
    get_detail(sent)
    root = get_noun_chunk(sent)
    keywords.append(root)


print("\n", keywords)