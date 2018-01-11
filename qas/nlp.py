import spacy

try:
    nlp = spacy.load('en_core_web_md')
except ImportError:
    nlp = spacy.load('en')