from wiki.wiki_query import WikiQuery
from wiki.wiki_fetch import WikiFetch
from wiki.wiki_parse import XPathExtractor

import logging

logger = logging.getLogger(__name__)


class SearchSources:

    source_type = "wiki"
    search_keywords = []
    max_page_per_search = 10

    def __init__(self, search_keywords, source_type, max_page_per_search):
        self.search_keywords = search_keywords
        self.source_type = source_type
        self.max_page_per_search = max_page_per_search

    def query_source(self):
        if self.source_type == "wiki":
            for keyword in self.search_keywords:
                logger.info("Searching:{0}".format(keyword))
                wikiq = WikiQuery(keyword, self.max_page_per_search)
                wiki_page_ids = wikiq.fetch_wiki_pages()
                wikif = WikiFetch(wiki_page_ids)
                wikif.parse_wiki_page()
                for page in wiki_page_ids:
                    xpe = XPathExtractor(page)
                    xpe.strip_tag()
                    xpe.strip_headings()
                    extracted_img = xpe.img_extract()
                    extracted_info = xpe.extract_info()
                    extracted_table = xpe.extract_tables()
                    extracted_text = xpe.extract_text()
        else:
            print("Source not supported")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    search = ['albert einstein', 'birth']
    sr = SearchSources(search, "wiki", 3)
    sr.query_source()