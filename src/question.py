# This file process the question

# ----------Imports------------

import re

# -----------------------------

question = raw_input("Q:")
question = question.lower()

symbols = re.findall(r'\W(?!\w)', question)
for sym in range(len(symbols)):
    question = question.replace(symbols[sym], " "+symbols[sym])

que_list = re.compile("\s+").split(question)

print(que_list)
