'''

Feature Extractor

Based on Question Type
Feature Extraction

Candidate selection: Here, we extract all possible words, phrases, terms or concepts (depending on the task) that can potentially be keywords.
Properties calculation: For each candidate, we need to calculate properties that indicate that it may be a keyword.
Scoring and selecting keywords: All candidates can be scored by either combining the properties into a formula, or using a machine learning technique to determine probability of a candidate being a keyword

'''

import spacy
import csv


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
                token_text = get_compound_nouns(token, token.text)
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


def write_csv(question, qclass, keywords):
    with open('corpus/feature_trainer.csv', 'a', newline='') as csv_fp:
        csv_fp_writer = csv.writer(csv_fp, delimiter='|')
        csv_fp_writer.writerow([question, qclass, keywords])
        csv_fp.close()


def process_question(question, qclass, en_nlp):

    en_doc = en_nlp(u'' + question)
    keywords = []

    for sent in en_doc.sents:
        # get_detail(sent)
        root, keywords = get_noun_chunk(sent, en_doc, keywords)
        keywords.append(root)

    write_csv(question, qclass, keywords)
    # print(keywords)
    del keywords[:]


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
    with open('corpus/feature_trainer.csv', 'w', newline='') as csv_fp:
        csv_fp_writer = csv.writer(csv_fp, delimiter='|')
        csv_fp_writer.writerow(['Question', 'Class', 'Keywords'])
        csv_fp.close()

clean_old_data()
en_nlp = spacy.load('en_core_web_md')

with open('corpus/qclassification_data.txt', 'r') as fp:
    read_input_file(fp, en_nlp)
    fp.close()
    print("CSV Data Trained...")