import requests
import bs4


search_term = input("Enter Search Term:")
search_term.replace("", "_")
wiki_url = "https://en.wikipedia.org/wiki/"+search_term
# wiki_url = "https://en.wikipedia.org/wiki/Terra"

html_response = requests.get(wiki_url)
# print(html_respose.content)

search_results = {}

soup = bs4.BeautifulSoup(html_response.content, 'lxml')
soup.find('div', class_='toc').decompose()

# print(soup.prettify())

content = soup.find('div', class_='mw-content-ltr')

disambiguation = bs4.BeautifulSoup(str(content), 'lxml')
candidates = disambiguation.find_all('p')
for i in range(len(candidates)):

    if candidates[i].find('a'):
        # print("https://en.wikipedia.org"+candidates[i].find('a').get('href'))
        url = "https://en.wikipedia.org"+candidates[i].find('a').get('href')
        search_results[i] = url
        print("[", i, "]", candidates[i].get_text())
    else:
        print(candidates[i].get_text())

categories = disambiguation.find_all('h2')
for i in range(len(categories)):
    if categories[i].find_next().get_text() != "References" and categories[i].find_next().get_text() != "See also":
        print("[", i + 1, "]", categories[i].find_next().get_text(), ":")
        # print(categories[i].find_next_sibling().get_text())
        category_content = categories[i].find_next_sibling()
        category_content_item = category_content.find_all('li')
        for j in range(len(category_content_item)):
            print(i + 1, ".", j + 1, ")", category_content_item[j].get_text())
            # print("https://en.wikipedia.org"+category_content_item[j].find('a').get('href'))
            index = float(str(i+1)+"."+str(j+1))
            url = "https://en.wikipedia.org"+category_content_item[j].find('a').get('href')
            search_results[index] = url

result_index = input("Select a search result:")
if search_results[float(result_index)]:
    print(search_results[float(result_index)])
else:
    print("Error Not Found")
