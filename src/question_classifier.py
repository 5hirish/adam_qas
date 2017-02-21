import spacy

"""
WH Bi-gram
Root word = Part of Speech
Bi-gram = Part of Speech
"""

question = "How did serfdom develop in and then leave Russia ?"

en_nlp = spacy.load("en")
en_doc = en_nlp(u'' + question)
for sent in en_doc.sents:
    wh_bi_gram = []
    root_token = ""
    wh_pos = ""
    wh_nbor_pos = ""
    for token in sent:
        if token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
            wh_pos = token.tag_
            wh_bi_gram.append(token.text)
            wh_bi_gram.append(str(en_doc[token.i + 1]))
            wh_nbor_pos = en_doc[token.i + 1].tag_
        if token.dep_ == "ROOT":
            root_token = token.tag_

    print(wh_pos, wh_nbor_pos)
    print(wh_bi_gram)
    print(root_token)
