from unittest import TestCase
from qas.wiki.wiki_query import WikiQuery
from qas.wiki.wiki_fetch import WikiFetch
from qas.wiki.wiki_parse import XPathExtractor

from qas.esstore.es_operate import ElasticSearchOperate
from qas.esstore.es_config import __wiki_title__, __wiki_raw__, __wiki_revision__


class TestWikiScraper(TestCase):

    es_ops = None
    page_list = []

    def __init__(self, *args, **kwargs):
        super(TestWikiScraper, self).__init__(*args, **kwargs)
        self.es_ops = ElasticSearchOperate()

    def test_query_wiki_pages(self):
        html_tag_expr = '<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>(.*?)</\1>'

        query_set = ["Alan Turing", "Harry Potter and the Deathly Hallows", "Tiger", "Melbourne"]

        for query in query_set:
            wikiq = WikiQuery(query)
            self.page_list = wikiq.fetch_wiki_pages()
            assert len(self.page_list) == wikiq.wiki_max_results

            with self.subTest(query):
                wikif = WikiFetch(self.page_list)
                wikif.parse_wiki_page()

                for pageid in self.page_list:
                    with self.subTest(pageid):
                        wiki_data = self.es_ops.get_wiki_article(pageid)
                        assert wiki_data is not None
                        assert wiki_data[__wiki_title__]
                        assert wiki_data[__wiki_raw__]
                        assert wiki_data[__wiki_revision__]

                for page in self.page_list:
                    with self.subTest(page):
                        xpe = XPathExtractor(page)
                        xpe.strip_tag()
                        xpe.strip_headings()
                        img = xpe.img_extract()
                        info = xpe.extract_info()
                        table = xpe.extract_tables()
                        text = xpe.extract_text()
                        self.assertNotRegex(text, html_tag_expr)

