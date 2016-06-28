# ----------Imports------------

import re
import nltk
import os

# -----------------------------

path = os.path.dirname(os.path.realpath(__file__))
path = path.replace("/src", "/corpora/")
fp = open(path+"regdata.txt", "r")

# print classifications[class_type.lower()]
for line in fp:
    confidence = 0
    #sentence = re.compile("([A-z](?:\.|\?) )").split(line)
    #sentence = re.compile("\.\s(?=[A-z])").split(line)
    sentence = line.split(". ")
    #sentence = nltk.tokenize.sent_tokenize(line)
    for sent in sentence:
        print sent


fp.close()

