import requests
import json

# search_term = input("Enter Search term")
search_term = 'tiger'
wiki_rest_api = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srnamespace=0&srprop=timestamp&&srsearch=intitle:tiger'
print(wiki_rest_api)
wiki_response = requests.get(wiki_rest_api)
wiki_json_response = wiki_response.json()
print(wiki_json_response)

