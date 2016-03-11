# This file process the question

# ----------Imports------------

import re
import nltk
#from nltk.tag.stanford import StanfordPOSTagger

# -----------------------------

question = raw_input("Q:")
question = question.lower()                                             # Convert to lower case

symbols = re.findall(r'\W(?!\w)', question)                             # Separate symbols
for sym in range(len(symbols)):
    question = question.replace(symbols[sym], " "+symbols[sym])

que_list = re.compile("\s+").split(question)                            # Split by space

print(que_list)

pos = nltk.pos_tag(que_list)

print pos

st = StanfordPOSTagger(r'/home/amit/stanford-postagger/models/english-bidirectional-distsim.tagger',r'/home/amit/stanford-postagger/stanford-postagger.jar')
''' error comes here in st.tag instruction  '''

#print st.tag('What is the airspeed of an unladen swallow ?'.split())


#forget about this ----> this is output--->[(u'What', u'WP'), (u'is', u'VBZ'), (u'the', u'DT'), (u'airspeed', u'NN'), (u'of', u'IN'), (u'an', u'DT'), (u'unladen', u'JJ'), (u'swallow', u'VB'), (u'?', u'.')]

