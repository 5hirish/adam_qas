import wikipedia
from collections import OrderedDict


def search_wiki(keywords, number_of_search, wiki_pages):
    suggestion = False

    for word in range(0, len(keywords) - 1):
        # print(keywords[word], ">>")
        result_set = wikipedia.search(keywords[word], number_of_search, suggestion)
        for term in result_set:
            page = wikipedia.page(term, preload=False)
            page_title = page.title
            page_summary = page.summary
            page_content = page.content

            wiki_pages[page_title] = page_content

            # print(page_title, len(page_content), type(page_content))

    return wiki_pages


def fetch_wiki(keywords, number_of_search):

    wiki_pages = OrderedDict()

    search_wiki(keywords, number_of_search, wiki_pages)

    # print(wiki_pages)

    return wiki_pages
