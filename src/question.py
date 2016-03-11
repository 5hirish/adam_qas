# This file process the question

# ----------Imports------------

import re
import nltk

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

#from nltk.tag.stanford import StanfordPOSTagger
#st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
#print st.tag('What is the airspeed of an unladen swallow ?'.split())
#[(u'What', u'WP'), (u'is', u'VBZ'), (u'the', u'DT'), (u'airspeed', u'NN'), (u'of', u'IN'), (u'an', u'DT'), (u'unladen', u'JJ'), (u'swallow', u'VB'), (u'?', u'.')]

