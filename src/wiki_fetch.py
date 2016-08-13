import requests
import bs4

html_respose = requests.get('https://en.wikipedia.org/wiki/Terra')
# print(html_respose.content)

soup = bs4.BeautifulSoup(html_respose.content, 'lxml')
soup.find('div', class_='toc').decompose()

# print(soup.prettify())

# content = soup.find_all("div", class_="mw-body")
# print(content)

content = soup.find_all('div', class_='mw-content-ltr')
content_html = ''

for elements in content:
    content_html = content_html.join(str(elements))

disambiguation = bs4.BeautifulSoup(content_html, 'lxml')
candidates = disambiguation.find_all('p')
for elements in candidates:
    print(elements)

categories = disambiguation.find_all('span', class_='mw-headline')
categories_content = disambiguation.find_all('ul')
for elements, elements_content in zip(categories, categories_content):
    print(elements)
    print(elements_content)