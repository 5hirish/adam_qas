#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys

import spacy

from qas import __version__
from qas.candidate_ans import get_candidate_answers
from qas.classifier.question_classifier import classify_question
from qas.constants import EN_MODEL_MD, EN_MODEL_DEFAULT, EN_MODEL_SM
from qas.doc_search_rank import search_rank
from qas.feature_extractor import extract_features
from qas.query_const import construct_query
from qas.wiki.wiki_search import search_wikipedia

__author__ = "Shirish Kadam"
__copyright__ = "Copyright (C) 2017  Shirish Kadam"
__license__ = "GNU General Public License v3 (GPLv3)"

_logger = logging.getLogger(__name__)


def get_default_model(model_name):
    err_msg = "Language model {0} not found. Please, refer https://spacy.io/usage/models"
    nlp = None
    if model_name is not None:
        try:
            nlp = spacy.load(model_name)
        except (ImportError, OSError):
            print(err_msg.format(model_name))
            print('Using default language model')
            nlp = get_default_model(EN_MODEL_SM)
        return nlp


def get_nlp(language, lite, lang_model=""):
    err_msg = "Language model {0} not found. Please, refer https://spacy.io/usage/models"
    nlp = None

    if not lang_model == "" and not lang_model == "en":

        try:
            nlp = spacy.load(lang_model)
        except ImportError:
            print(err_msg.format(lang_model))
            raise

    elif language == 'en':

        if lite:
            nlp = spacy.load(EN_MODEL_DEFAULT)
        else:

            try:
                nlp = spacy.load(EN_MODEL_MD)
            except (ImportError, OSError):
                print(err_msg.format(EN_MODEL_MD))
                print('Using default language model')
                nlp = get_default_model(EN_MODEL_DEFAULT)

    elif not language == 'en':
        print('Currently only English language is supported. '
              'Please contribute to https://github.com/5hirish/adam_qas to add your language.')
        sys.exit(0)

    return nlp


class QasInit:

    nlp = None
    language = "en"
    lang_model = None
    search_depth = 3
    lite = False

    question_doc = None

    question_class = ""
    question_keywords = None
    query = None

    candidate_answers = None

    def __init__(self, language, search_depth, lite, lang_model=""):
        self.language = language
        self.search_depth = search_depth
        self.lite = lite
        self.lang_model = lang_model
        self.nlp = get_nlp(self.language, self.lite, self.lang_model)

    def get_question_doc(self, question):

        self.question_doc = self.nlp(u'' + question)

        return self.question_doc

    def process_question(self):

        self.question_class = classify_question(self.question_doc)
        _logger.info("Question Class: {}".format(self.question_class))

        self.question_keywords = extract_features(self.question_class, self.question_doc)
        _logger.info("Question Features: {}".format(self.question_keywords))

        self.query = construct_query(self.question_keywords, self.question_doc)
        _logger.info("Query: {}".format(self.query))

    def process_answer(self):

        _logger.info("Retrieving {} Wikipedia pages...".format(self.search_depth))
        search_wikipedia(self.question_keywords, self.search_depth)

        # Anaphora Resolution
        wiki_pages = search_rank(self.query)
        _logger.info("Pages retrieved: {}".format(len(wiki_pages)))

        self.candidate_answers, keywords = get_candidate_answers(self.query, wiki_pages, self.nlp)
        _logger.info("Candidate answers ({}):\n{}".format(len(self.candidate_answers), '\n'.join(self.candidate_answers)))

        return " ".join(self.candidate_answers)


def parse_args(args):

    parser = argparse.ArgumentParser(
        description="Adam a question answering system")

    parser.add_argument(
        '--version',
        action='version',
        help="show version",
        version='qas {ver}'.format(ver=__version__))

    parser.add_argument(
        dest="question",
        help="Question for the Know It All Adam to answer",
        type=str,
        default='',
        metavar='"QUESTION"')

    parser.add_argument(
        '-l',
        '--lang',
        dest="language",
        help="set language according to ISO codes",
        default='en',
        type=str,
        metavar="XX"
    )

    parser.add_argument(
        '-n',
        dest="search_limit",
        help="set limit for pages fetched from Wikipedia. Default is 3 and max is 10",
        default=3,
        type=int,
        metavar="Y"
    )

    parser.add_argument(
        '--lite',
        action='store_const',
        dest="lite",
        default=False,
        const=True,
        help="set qas to use lighter version of language model"
    )

    parser.add_argument(
        '--model',
        dest="lang_model",
        default="en",
        type=str,
        help="set spaCy language model",
        metavar="XXX_XX"
    )

    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)

    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)

    # parser.print_help()

    return parser.parse_args(args)


def setup_logging(loglevel):

    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('elasticsearch').setLevel(logging.CRITICAL)
    logging.getLogger('gensim').setLevel(logging.CRITICAL)


def main(args):

    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Thinking...")
    if args.question is None:
        args.question = input("Ask your question:>")

    print("I think what you want to know is: {}".format(args.question))

    # print(args)

    qas = QasInit(language=args.language, search_depth=args.search_limit, lite=args.lite, lang_model=args.lang_model)
    qas.get_question_doc(args.question)
    qas.process_question()
    answer = qas.process_answer()
    #
    print("\n\n** Your answer:\n {}".format(answer))


def run():

    main(sys.argv[1:])


if __name__ == "__main__":
    run()
