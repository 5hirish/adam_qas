import wikipedia
from collections import OrderedDict

keywords = ['species', 'Great White shark', 'are']
wiki_pages = OrderedDict()

number_of_search = 3
suggestion = False


def search_wiki(keywords):

    for word in range(0, len(keywords) - 1):
        print(keywords[word], ">>")
        result_set = wikipedia.search(keywords[word], number_of_search, suggestion)
        for term in result_set:
            page = wikipedia.page(term, preload=False)
            page_title = page.title
            page_summary = page.summary
            page_content = page.content

            wiki_pages[page_title] = page_content

            print(page_title, len(page_content), type(page_content))

    print(wiki_pages)


search_wiki(keywords)
print("------")
