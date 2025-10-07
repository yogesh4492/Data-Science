import json
import requests

def fetch_and_print_articles(api_url):
    response = requests.get(api_url)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        
        for index, article in enumerate(articles[:1], start=1):
            print(f"Article {index}:\n{json.dumps(article, sort_keys=True, indent=4)}\n")
    else:
        print(f"Error: {response.status_code}")

API_KEY = 'd66ea8c899c4415d91f5301d8edc643d'
api_endpoint = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=%7BAPI_KEY%7D"

fetch_and_print_articles(api_endpoint)

def jprint(obj):
    print(json.dumps(obj, sort_keys=True, indent=4))