import requests
import sys
import logging
from lxml import etree

from qas.constants import OUTPUT_DIR, SAVE_OUTPUTS
from qas.esstore.es_operate import ElasticSearchOperate
"""
https://en.wikipedia.org/w/api.php [EndPoint] [User-Agent header]
 > format:json
 > action:parse

    pageid: Parse the content of this page. Overrides page.

    prop:text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties|parsewarnings

 eg: https://en.wikipedia.org/w/api.php?action=parse&pageid=16283969
 doc: https://en.wikipedia.org/w/api.php?action=help&modules=parse

"""

logger = logging.getLogger(__name__)


class WikiFetch:

    base_url = 'https://en.wikipedia.org/w/api.php'
    # noinspection PyDictCreation
    wiki_query_payload = {'action': 'parse', 'format': 'json'}
    wiki_query_payload['prop'] = 'text|links|images|externallinks|sections|revid|displaytitle|iwlinks'
    es_ops = None
    page_list = []
    wiki_text = []

    def __init__(self, page_list):
        self.page_list = page_list
        self.es_ops = ElasticSearchOperate()

    def parse_wiki_page(self):

        for page in self.page_list:

            self.wiki_query_payload['pageid'] = page

            wiki_query_req = requests.get(self.base_url, params=self.wiki_query_payload)
            wiki_query_response = wiki_query_req.json()
            wiki_revid = wiki_query_response.get('parse').get('revid')
            wiki_title = wiki_query_response.get('parse').get('title')
            wiki_html_text = wiki_query_response.get('parse').get('text').get('*')

            res = self.es_ops.upsert_wiki_article_if_updated(page, wiki_revid, wiki_title, wiki_html_text)
            if res:
                logger.info("Wiki article {0} inserted.".format(page))
            else:
                logger.error("Wiki article insertion failed")

            self.wiki_text.append(wiki_html_text)
        return self.wiki_text

    @staticmethod
    def save_html(content, page):
        parser = etree.XMLParser(ns_clean=True, remove_comments=True)
        html_tree = etree.fromstring(content, parser)
        html_str = etree.tostring(html_tree, pretty_print=True)
        with open(OUTPUT_DIR + '/wiki_content_'+str(page)+'.html', 'wb') as fp:
            fp.write(html_str)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        parse_pageId = sys.argv[1:]
        wikif = WikiFetch(parse_pageId)
        html_text = wikif.parse_wiki_page()

        if SAVE_OUTPUTS:
            for pageId, text in zip(parse_pageId, html_text):
                WikiFetch.save_html(text, pageId)

    else:
        raise ValueError('No page id provided for Wiki parse')
