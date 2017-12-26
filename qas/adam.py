#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.cfg:

    console_scripts =
     fibonacci = qas.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""
from __future__ import division, print_function, absolute_import

import argparse
import re
import sys
import logging

import enchant
import autocorrect

from qas.qclassifier import classify_question
from qas.feature_extractor import extract_features
from qas.query_const import construct_query
from qas.fetch_wiki import fetch_wiki
from qas.doc_scorer import rank_docs
from qas.candidate_ans import get_candidate_answers
from qas.constants import nlp, EXAMPLE_QUESTIONS
from qas import __version__

__author__ = "Shirish Kadam"
__copyright__ = "Copyright (C) 2017  Shirish Kadam"
__license__ = "GNU General Public License v3 (GPLv3)"

_logger = logging.getLogger(__name__)


def answer_question(q, num_sentences):

    q = nlp(u'' + q)

    question_class = classify_question(q)
    _logger.info("Question Class: {}".format(question_class))

    question_keywords = extract_features(question_class, q)
    _logger.debug("Question Features: {}".format(question_keywords))

    query = construct_query(question_keywords, q)
    _logger.debug("Query: {}".format(query))

    _logger.info("Retrieving {} wikipedia pages...".format(num_sentences))
    wiki_pages = fetch_wiki(question_keywords, number_of_search=num_sentences)
    _logger.debug("Pages retrieved: {}".format(len(wiki_pages)))

    # Anaphora Resolution

    ranked_wiki_docs = rank_docs(question_keywords)
    _logger.debug("Ranked pages: {}".format(ranked_wiki_docs))

    candidate_answers, keywords = get_candidate_answers(query, ranked_wiki_docs, nlp)
    _logger.info("Candidate answers ({}):\n{}".format(len(candidate_answers), '\n'.join(candidate_answers)))

    return " ".join(candidate_answers)


en_dict = enchant.Dict("en_US")


def is_spelled_correctly(word):
    return re.match(r'\w', word) is None or en_dict.check(word)


def correct_spelling(s):
    return " ".join([(autocorrect.spell(w) if not is_spelled_correctly(w) else w) for w in s.split()])


def answer(q):
    """ Find the answer to a natural language query in Wikipedia, etc

    Args:
      q (str): Quetsion to be answered by searching Wikipedia

    Returns:
      str: Answer to the question posed
    """


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Adam a question answering system")
    parser.add_argument(
        '--version',
        action='version',
        version='qas {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="question",
        help="Question for the Know It All Adam to answer",
        type=str,
        default='',
        metavar="STR")
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
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Thinking...")
    print("I think what you want to know is {}".format((args.question)))


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
