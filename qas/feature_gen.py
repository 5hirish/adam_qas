import spacy

"""
Question Type
Part of Speech
Dependency
Entity
Shape

Class - F / NF
"""


def process_question(question, qclass, en_nlp):
    en_doc = en_nlp(u'' + question)
    sent_list = list(en_doc.sents)
    sent = sent_list[0]

    feat_class = "F"

    for token in sent:
        feat = token.text
        feat_pos = token.tag_
        feat_dep = token.dep_
        feat_ent_label = token.ent_type_
        feat_shape = token.shape_

        if feat_ent_label == "":
            feat_ent_label = "NON"

        output = [question, qclass, feat_pos, feat_dep, feat_ent_label, feat_shape, feat, feat_class]
        print("|".join(output))


en_nlp = spacy.load("en_core_web_md")

question = "Who was The Pride of the Yankees ?"
qclass = "DESC"
process_question(question, qclass, en_nlp)

