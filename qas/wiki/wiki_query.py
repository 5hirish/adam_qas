import requests
import urllib.parse
import sys
import logging

"""
https://en.wikipedia.org/w/api.php [EndPoint] [User-Agent header]
 > format:json
 > action:query

    list:search

    srsearch: Search for all page titles (or content) that have this value.
    srwhat: Search inside the text or titles.
    srlimit: How many total pages to return. No more than 50 (500 for bots) allowed. (Default: 10)

    prop:

 eg: https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&utf8=1&srsearch=Albert%20Einstein
 eg: https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=wikipedia&srwhat=text
 doc: https://en.wikipedia.org/w/api.php?action=help&modules=query
"""


class WikiQuery:

    base_url = 'https://en.wikipedia.org/w/api.php'
    wiki_max_results = 10

    # noinspection PyDictCreation
    wiki_query_payload = {'action': 'query', 'format': 'json', 'list': 'search'}
    wiki_query_payload['srwhat'] = 'text'
    wiki_query_payload['srlimit'] = str(wiki_max_results)
    search_term = ""

    def __init__(self, search_term):
        self.search_term = search_term

    def fetch_wiki_pages(self):

        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        search_term = urllib.parse.quote(self.search_term)
        logger.debug("Querying: %s", search_term)

        self.wiki_query_payload['srsearch'] = search_term

        wiki_query_req = requests.get(self.base_url, params=self.wiki_query_payload)
        wiki_query_response = wiki_query_req.json()

        if 'errors' not in wiki_query_response:
            wiki_page_list = wiki_query_response.get('query').get('search')
            pages_list = [pages.get('pageid') for pages in wiki_page_list]
            logger.debug("Fetched %d : %s", len(pages_list), str(pages_list))
            return pages_list

        else:
            logger.error(wiki_query_req.text)
            return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_term_cmd = " ".join(sys.argv[1:])
        wikiq = WikiQuery(search_term_cmd)
        print(wikiq.fetch_wiki_pages())

    else:
        raise ValueError('No search term provided for Wiki query')
