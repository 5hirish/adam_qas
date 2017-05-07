'''

The Query is constructed just to show relationship amongst different features in the feature set.
A conjunction is a part of speech that is used to connect words, phrases, clauses, or sentences. 

'''

import spacy
import csv


def get_detail(sent):
    for token in sent:
        print(token.text, token.lemma_, token.tag_, token.ent_type_, token.dep_, token.head)


question = "What are Cushman or Wakefield known for ?"
features = ['Cushman', 'known', 'Wakefield', 'are']

en_nlp = spacy.load('en_core_web_md')

en_doc = en_nlp(u'' + question)


def get_conjuncts(token):
    parent = token.head
    conj = [parent.text]

    for child in parent.children:
        if child.dep_ == "conj":
            conj.append(child.text)

    print(conj)
    return conj


def get_query(sent, features):

    conjunct_list = []
    neg_list = []
    mark_list = []
    for token in sent:
        if token.dep_ == "cc":
            print(token.i, token.text)
            conjunct_list.append(get_conjuncts(token))
            conjunct_list.append(token.text)

        if token.dep_ == "neg":
            if token.i > token.head.i:
                neg_list.append([token.text, token.head.text])
                print(token.text, token.head.text)
            else:
                neg_list.append([token.head.text, token.text])
                print(token.head.text, token.text)

        if token.dep_ == "mark":
            if token.i > token.head.i:
                mark_list.append([token.text, token.head.text])
                print(token.text, token.head.text)
            else:
                mark_list.append([token.head.text, token.text])
                print(token.head.text, token.text)

    return [features, conjunct_list, neg_list, mark_list]

query = []

for sent in en_doc.sents:
    get_detail(sent)
    query = get_query(sent, features)

    print(query)
