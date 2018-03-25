import logging
import csv

from qas.constants import CORPUS_DIR
from qas.corpus.data import WIKI_QA_TSV
from qas.sqlitestore.sqlt_connect import SqLiteManager

"""
Created by felix on 11/3/18 at 5:50 PM
"""

logger = logging.getLogger(__name__)


# Dataset from WikiQA.tsv. Beware this file is of type TSV
# Warning: This will remove old results and give you a fresh start.

def insert_question_to_sqlt():
    question_set = []
    last_question = ""
    with open(CORPUS_DIR+"/"+WIKI_QA_TSV) as file:
        wiki_file = csv.DictReader(file, dialect='excel-tab')
        if wiki_file is not None:
            for row in wiki_file:
                if row['Question'] != last_question:
                    question = (row['Question'], )
                    question_set.append(question)
                    last_question = row['Question']

    if question_set is not None:
        sqlt_man = SqLiteManager()
        # sqlt_man.remove_old_results()
        sqlt_man.remove_all_data()
        logger.info("Removed Old test results")
        sqlt_man.insert_many_question(question_set)
        logger.info("Inserted {0} questions".format(sqlt_man.get_question_count()))


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    insert_question_to_sqlt()