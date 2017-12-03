import spacy
import csv

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
        if token.pos_ == "NOUN" or token.pos_ == "PROPN" or token.pos_ == "VERB" or token.pos_ == "NUM" or token.pos_ == "ADJ" or token.pos_ == "ADV":
            if token.tag_ != "WDT" and token.tag_ != "WP" and token.tag_ != "WP$" and token.tag_ != "WRB" and token.dep_ != "ROOT":
                feat = token.text
                feat_pos = token.tag_
                feat_dep = token.dep_
                feat_ent_label = token.ent_type_
                feat_shape = token.shape_

                if feat_ent_label == "":
                    feat_ent_label = "NON"

                # print(token.text, "-", feat_pos, token.pos_, feat_dep, feat_ent_label, feat_shape)

                with open('corpus/feature_trainer.csv', 'a', newline='') as csv_fp:
                    csv_fp_writer = csv.writer(csv_fp, delimiter='|')
                    csv_fp_writer.writerow([question, qclass, feat_pos, feat_dep, feat_ent_label, feat_shape, feat, feat_class])
                    csv_fp.close()


def read_input_file(fp, en_nlp):

    for _ in range(200):
        next(fp)

    for line in fp:
        line = line.strip("\n")
        list_line = line.split("|")
        question = list_line[0]
        qclass = list_line[len(list_line) - 1]
        if not question.startswith("#"):
            # print(qclass, question)
            process_question(question, qclass, en_nlp)


def clean_old_data():
    with open('corpus/feature_trainer.csv', 'w', newline='') as csv_fp:
        csv_fp_writer = csv.writer(csv_fp, delimiter='|')
        csv_fp_writer.writerow(['#Question', 'QType', 'F-POS', 'F-DEP', 'F-ENT', 'F-SHAPE', 'F-TXT', 'Class'])
        csv_fp.close()


clean_old_data()
en_nlp = spacy.load("en_core_web_md")

with open('corpus/qclassifier_trainer.csv', 'r') as fp:
    read_input_file(fp, en_nlp)
    fp.close()
    print("CSV Data Trained...")

print("Remove Noisy Data... by ||||")