""" Package Global Constants """
import os

import spacy


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORPUS_DIR = os.path.join(os.path.dirname(__file__), 'corpus')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
EXAMPLE_QUESTIONS = [
    "What's Eddie Vedder's most famous song?",
    "Who's Barak Obama?",
    "Where is Pascagoula?",
    'Which states have a city called "Hot Coffee"?',
    "Is Santa Claus real?",
    "Is ice hot or cold?",
    "Who was a better baseball player, Johny Cash or Babe Ruth?"
    "How many states are in the US?",
    "How old is Hillary Clinton?",
    "Where do babies come from?",
    "How often is the moon full in a year?",
    "How far is Mars from Earth?",
    "How many people are in China?",
    "How many blind or visually impaired people live in Europe?"]


# nlp = spacy.load('en_core_web_md')
