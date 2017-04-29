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
        print(token.text, token.lemma_, token.tag_, token.ent_type_, token.dep_, token.head)


def get_compound_nouns(token, token_text):

    for child in token.children:

        # print(child.text, child.dep_)

        if child.dep_ == "compound":
            token_text = child.text + " " + token_text
            token_text = get_compound_nouns(child, token_text)

    return token_text


def get_adj_phrase(token, token_text):
    # print(token.text)
    for child in token.children:
        if child.dep_ == "amod" or child.dep_ == "acomp" or child.dep_ == "ccomp":  # not for how many
            if child.text != "much" and child.text != "many":
                token_text = child.text + " " + token_text
    return token_text


def get_root_phrase(token):
    for child in token.children:
        if child.dep_ == "acomp" or child.dep_ == "xcomp" or child.dep_ == "ccomp":
            keywords.append(child.text)


def get_noun_chunk(sent, en_doc):
    root = ""
    for token in sent:
        if token.tag_ == "NN" or token.tag_ == "NNP" or token.tag_ == "NNPS" or token.tag_ == "NNS":
            if token.dep_ != "compound":
                token_text = get_compound_nouns(token, token.text)
                token_text = get_adj_phrase(token, token_text)
                keywords.append(token_text)

        if token.dep_ == "nummod" or token.tag_ == "CD":
            token_text = token.text
            if token.i > 0:
                if en_doc[token.i - 1].tag_ == "JJ":
                    token_text = en_doc[token.i - 1].text + " " + token.text
            if token.i < len(en_doc):
                if en_doc[token.i + 1].tag_ == "JJ":
                    token_text = token.text + " " + en_doc[token.i + 1].text
            keywords.append(token_text)

        if token.dep_ == "ROOT":
            root = token.text
            get_root_phrase(token)

    return root


# text = "What team did baseball's St. Louis Browns become ?"
# text = "What contemptible scoundrel stole the cork from my lunch ?"
# text = "What fowl grabs the spotlight after the Chinese Year of the Monkey ?"
# text = "What is an annotated bibliography ?"
# text = "What is the origin of the name ' Scarlett ' ?"
# text = "How much would it cost to purchase a 2-foot-square party tent , with sides , ?"
text = input("Q:")

en_nlp = spacy.load('en')
# print(spacy.info('en')) core_web_sm
en_doc = en_nlp(u'' + text)
keywords = []

for sent in en_doc.sents:
    get_detail(sent)
    root = get_noun_chunk(sent, en_doc)
    keywords.append(root)


print("\n", keywords)