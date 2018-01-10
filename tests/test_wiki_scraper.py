from unittest import TestCase
from qas.wiki.wiki_query import WikiQuery


class TestWikiScraper(TestCase):

    def test_fetch_wiki_pages(self):
        query_set = ["Alan Turing", "Harry Potter and the Deathly Hallows", "Tiger", "Melbourne"]
        for query in query_set:
            wikiq = WikiQuery(query)
            page_list = wikiq.fetch_wiki_pages()
            assert len(page_list) == wikiq.wiki_max_results
