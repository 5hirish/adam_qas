# ----------Imports------------

import re
import nltk
import os

# -----------------------------

def sent_split(sent):

    sent = sent.lower()                                             # Convert to lower case

    symbols = re.findall(r'\W(?!\w)', sent)                             # Separate symbols
    for sym in range(len(symbols)):
        sent = sent.replace(symbols[sym], " "+symbols[sym])

    sent_list = re.compile("\s+").split(sent)                            # Split by space

    return sent_list

focus = raw_input("Focus:")
action = raw_input("Action: ")
class_type = raw_input("Type:")
classifications = {"what": "action", "when": "time", "where": "place", "who": "person", "whom": "object", "which": "choice", "whose": "possession", "why": "reason", "how": "manner"}

# test = "Hi Shirish how are you?"

path = os.path.dirname(os.path.realpath(__file__))
path = path.replace("/src", "/corpus/")
fp = open(path+"linus_torvalds.txt", "r")

# print classifications[class_type.lower()]

"""if test.lower().find(focus.lower()) != -1:
    if test.lower().find(action.lower()) != -1:
        print(test)"""

for line in fp:
    confidence = 0
    sentence = line.split(". ")                                                             # Fix this...

    for sent in sentence:
        if sent.lower().find(focus.lower()) != -1:
            confidence += 1
            print "Candidates: "+sent
            if sent.lower().find(action.lower()) != -1:
                print "Final Answer: ", sent
                confidence += 1
                print("Confidence rate: ", confidence)
                sent_list = sent_split(sent)
                pos = nltk.pos_tag(sent_list)
                print pos

fp.close()
