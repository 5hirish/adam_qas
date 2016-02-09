# This file process the question

# ----------Imports------------

import re

# -----------------------------

question = raw_input("Q:")
question = question.lower()                                             # Convert to lower case

symbols = re.findall(r'\W(?!\w)', question)                             # Separate symbols
for sym in range(len(symbols)):
    question = question.replace(symbols[sym], " "+symbols[sym])

que_list = re.compile("\s+").split(question)                            # Split by space

print(que_list)
