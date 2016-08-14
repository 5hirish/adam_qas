import requests
import bs4

html_response = requests.get('https://en.wikipedia.org/wiki/Terra')
# print(html_respose.content)

soup = bs4.BeautifulSoup(html_response.content, 'lxml')
soup.find('div', class_='toc').decompose()

# print(soup.prettify())

content = soup.find('div', class_='mw-content-ltr')

disambiguation = bs4.BeautifulSoup(str(content), 'lxml')
candidates = disambiguation.find_all('p')
for i in range(len(candidates)):

    if candidates[i].find('a'):
        print("https://en.wikipedia.org"+candidates[i].find('a').get('href'))
        print("[", i, "]", candidates[i].get_text())
    else:
        print(candidates[i].get_text())

categories = disambiguation.find_all('h2')
for i in range(len(categories)):
    if categories[i].find_next().get_text() != "References" or categories[i].find_next().get_text() != "See also":
        print("[", i + 1, "]", categories[i].find_next().get_text(), ":")
        # print(categories[i].find_next_sibling().get_text())
        category_content = categories[i].find_next_sibling()
        category_content_item = category_content.find_all('li')
        for j in range(len(category_content_item)):
            print(i + 1, ".", j + 1, ")", category_content_item[j].get_text())
            # print("https://en.wikipedia.org"+category_content_item[j].find('a').get('href'))
