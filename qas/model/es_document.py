
from qas.esstore.es_config import __wiki_content__, __wiki_content_info__, __wiki_content_table__, \
    __wiki_raw__, __wiki_title__, __wiki_pageid__, __wiki_revision__, __wiki_updated_date__

"""
Created by felix on 24/3/18 at 10:26 PM
"""


class ElasticSearchDocument:

    _source = None

    def __init__(self, article_id, source, score=0):
        self._source = dict()
        self._source[__wiki_pageid__] = article_id
        self._source['score'] = score
        self._source[__wiki_revision__] = source[__wiki_revision__]
        self._source[__wiki_updated_date__] = source[__wiki_updated_date__]
        self._source[__wiki_raw__] = source[__wiki_raw__]
        self._source[__wiki_title__] = source[__wiki_title__]
        self._source[__wiki_content__] = source[__wiki_content__]
        self._source[__wiki_content_info__] = source[__wiki_content_info__]
        self._source[__wiki_content_table__] = source[__wiki_content_table__]

    def get_wiki_revision(self):
        return self._source[__wiki_revision__]

    def get_wiki_article_id(self):
        return self._source[__wiki_pageid__]

    def get_wiki_updated_date(self):
        return self._source[__wiki_updated_date__]

    def get_wiki_raw_text(self):
        return self._source[__wiki_raw__]

    def get_wiki_title(self):
        return self._source[__wiki_title__]

    def get_wiki_content(self):
        return self._source[__wiki_content__]

    def get_wiki_content_info(self):
        return self._source[__wiki_content_info__]

    def get_wiki_content_table(self):
        return self._source[__wiki_content_table__]