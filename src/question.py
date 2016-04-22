# This file process the question

# ----------Imports------------

import time
import textblob
import spacy
import spacy.parts_of_speech

# -----------------------------



# -----------------------------


# question = raw_input("Q:")

start_time = time.time()

question = "Who is Linus Torvalds and where is he now?"
print "\n\t", question
doc = textblob.TextBlob(question)

print "\nSpell Correction:"
doc = doc.correct()
print doc

print "\nLanguage Detection:"
print doc.detect_language()

print "\nTranslated to Spanish:"
print doc.translate(from_lang='en', to='es')


print "\nPart of Speech Tagging:"
print doc.tags

print "\nNoun Phrase:"
print doc.noun_phrases

print "\nParsing:"
print doc.parse()

print "\nLemma:"
words = doc.words
for wd in words:
    print wd.lemmatize()
    # print wd.lemmatize('v')   # Lemmatize according to the Part of Speech
    # print wd.singularize(); print wd.puralize()


print("\n--- %s seconds ---" % (time.time() - start_time))
