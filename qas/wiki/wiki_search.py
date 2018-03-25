import sys
import logging

from qas.wiki.wiki_query import WikiQuery
from qas.wiki.wiki_fetch import WikiFetch
from qas.wiki.wiki_parse import extract_wiki_pages

"""
Created by felix on 24/3/18 at 10:55 PM
"""

logger = logging.getLogger(__name__)


def search_wikipedia(search_term_list, max_results):

    for search_term in search_term_list:
        wikiq = WikiQuery(search_term, max_results)
        wiki_page_ids = wikiq.fetch_wiki_pages()

        wikif = WikiFetch(wiki_page_ids)
        wikif.parse_wiki_page()

        extract_wiki_pages(wiki_page_ids)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) > 1:
        arguments = sys.argv
        search_wikipedia(arguments, 3)

    else:
        raise ValueError('Missing Arguments')