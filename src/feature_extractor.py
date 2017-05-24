import spacy
import csv


def get_detail(sent):
    for token in sent:
        print(token.text, token.lemma_, token.tag_, token.ent_type_, token.dep_, token.head)


def get_compound_nouns(en_doc, token, token_text):

    ptoken = token

    # print(token.text, token.dep_)
    while token.i > 0 and en_doc[token.i - 1].dep_ == "compound":           # token.shape_ == Xxxx... or XXXX... token.ent_iob_
        token_text = en_doc[token.i - 1].text + " " + token_text
        token = en_doc[token.i - 1]
        # print("L", token_text, type(en_doc[token.i - 1]))

    token = ptoken

    while token.i < len(en_doc) - 1 and en_doc[token.i + 1].dep_ == "compound":
        token_text = token_text + " " + en_doc[token.i + 1].text
        token = en_doc[token.i + 1]
        # print("R", token_text)

    return token_text


def get_adj_phrase(token, token_text):
    # print(token.text)
    for child in token.children:
        if child.dep_ == "amod" or child.dep_ == "acomp" or child.dep_ == "ccomp":  # not for how many
            if child.text != "much" and child.text != "many":
                token_text = child.text + " " + token_text
    return token_text


def get_root_phrase(token, keywords):
    for child in token.children:
        if child.dep_ == "acomp" or child.dep_ == "xcomp" or child.dep_ == "ccomp":
            keywords.append(child.text)
    return keywords


def get_noun_chunk(sent, en_doc, keywords):
    root = ""
    for token in sent:
        if token.tag_ == "NN" or token.tag_ == "NNP" or token.tag_ == "NNPS" or token.tag_ == "NNS":
            if token.dep_ != "compound":
                token_text = get_compound_nouns(en_doc, token, token.text)
                token_text = get_adj_phrase(token, token_text)
                keywords.append(token_text)

        if token.dep_ == "nummod" or token.tag_ == "CD":
            token_text = token.text
            if token.i > 0:
                if en_doc[token.i - 1].tag_ == "JJ":
                    token_text = en_doc[token.i - 1].text + " " + token.text
            if token.i < len(en_doc) - 1:
                if en_doc[token.i + 1].tag_ == "JJ":
                    token_text = token.text + " " + en_doc[token.i + 1].text
            keywords.append(token_text)

        if token.dep_ == "ROOT":
            root = token.text
            keywords = get_root_phrase(token, keywords)

    return root, keywords


def extract_features(qtype, en_doc):
    keywords = []

    for sent in en_doc.sents:
        # get_detail(sent)
        root, keywords = get_noun_chunk(sent, en_doc, keywords)
        keywords.append(root)

    return keywords

"""question = "What's the American dollar equivalent for 8 pounds in the U.K. ?"

en_nlp = spacy.load('en_core_web_md')

en_doc = en_nlp(u'' + question)
keywords = []

for sent in en_doc.sents:
    get_detail(sent)
    root, keywords = get_noun_chunk(sent, en_doc, keywords)
    keywords.append(root)

print(question)
print(keywords)"""
