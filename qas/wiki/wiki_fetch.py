import requests
import sys
import logging
from bs4 import BeautifulSoup
from qas.wiki.wiki_constants import base_url

"""
https://en.wikipedia.org/w/api.php [EndPoint] [User-Agent header]
 > format:json
 > action:parse

    pageid: Parse the content of this page. Overrides page.

    prop:text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties|parsewarnings

 eg: https://en.wikipedia.org/w/api.php?action=parse&pageid=16283969
 doc: https://en.wikipedia.org/w/api.php?action=help&modules=parse

"""


def parse_wiki_page(page_list):

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    for page in page_list:

        # noinspection PyDictCreation
        wiki_query_payload = {'action': 'parse', 'format': 'json'}
        wiki_query_payload['prop'] = 'text|links|images|externallinks|sections|displaytitle|iwlinks'
        wiki_query_payload['pageid'] = page

        wiki_query_req = requests.get(base_url, params=wiki_query_payload)
        wiki_query_response = wiki_query_req.json()
        wiki_html_text = wiki_query_response.get('parse').get('text').get('*')
        cleantext = BeautifulSoup(wiki_html_text, "lxml").text
        print(wiki_html_text)
        #print(cleantext) # Store in elasticsearch ... ?


if len(sys.argv) > 1:
    parse_pageId = sys.argv[1:]
    parse_wiki_page(parse_pageId)

else:
    raise ValueError('No page id provided for Wiki parse')
