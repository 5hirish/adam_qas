import spacy
import csv

"""
WH Bi-gram
Root word = Part of Speech
Bi-gram = Part of Speech
"""


def process_question(question, qclass, en_nlp):
    en_doc = en_nlp(u'' + question)
    sent_list = list(en_doc.sents)
    sent = sent_list[0]
    wh_bi_gram = []
    root_token = ""
    wh_pos = ""
    wh_nbor_pos = ""
    wh_word = ""
    for token in sent:
        if token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
            wh_pos = token.tag_
            wh_word = token.text
            wh_bi_gram.append(token.text)
            wh_bi_gram.append(str(en_doc[token.i + 1]))
            wh_nbor_pos = en_doc[token.i + 1].tag_
        if token.dep_ == "ROOT":
            root_token = token.tag_

        # print(wh_pos, wh_nbor_pos)
        # print(wh_bi_gram)
        # print(root_token)
    with open('corpus/qclassifier_trainer.csv', 'a', newline='') as csv_fp:
        csv_fp_writer = csv.writer(csv_fp, delimiter='|')
        csv_fp_writer.writerow([question, wh_word, " ".join(wh_bi_gram), wh_pos, wh_nbor_pos, root_token, qclass])
        csv_fp.close()


def read_input_file(fp, en_nlp):
    # question = "How did serfdom develop in and then leave Russia ?"
    for line in fp:
        list_line = line.split(" ")
        qclass_list = list_line[0].split(":")
        question = " ".join(list_line[1:len(list_line)])
        question = question.strip("\n")
        qclass = qclass_list[0]
        # print(qclass, question)
        process_question(question, qclass, en_nlp)


def clean_old_data():
    with open('corpus/qclassifier_trainer.csv', 'w', newline='') as csv_fp:
        csv_fp_writer = csv.writer(csv_fp, delimiter='|')
        csv_fp_writer.writerow(['Question', 'WH', 'WH-Bigram', 'WH-POS', 'WH-NBOR-POS', 'Root-POS', 'Class'])
        csv_fp.close()


clean_old_data()
en_nlp = spacy.load("en")

with open('corpus/qclassification_data.txt', 'r') as fp:
    read_input_file(fp, en_nlp)
    fp.close()
    print("CSV Data Trained...")

print("Remove Noisy Data... by ||||")



