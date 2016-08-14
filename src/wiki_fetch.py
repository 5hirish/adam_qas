import requests
import bs4

html_respose = requests.get('https://en.wikipedia.org/wiki/Terra')
# print(html_respose.content)

soup = bs4.BeautifulSoup(html_respose.content, 'lxml')
soup.find('div', class_='toc').decompose()

# print(soup.prettify())

# content = soup.find_all("div", class_="mw-body")
# print(content)

content = soup.find('div', class_='mw-content-ltr')

disambiguation = bs4.BeautifulSoup(str(content), 'lxml')
candidates = disambiguation.find_all('p')
for elements in candidates:
    print(elements)

categories = disambiguation.find_all('span', class_='mw-headline')
categories_content = disambiguation.find_all('ul')
"""for elements, elements_content in zip(categories, categories_content):
    print(elements)
    # print(elements_content)"""

"""test = disambiguation.find('h2')
print(test.find_next())
print(test.find_next_sibling())"""

test = disambiguation.find_all('h2')
for i in range(len(test)):
    print(test[i].find_next())
    print(test[i].find_next_sibling())
