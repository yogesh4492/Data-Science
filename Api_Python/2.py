import requests
import json
import csv
API_KEY='d66ea8c899c4415d91f5301d8edc643d'
url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=%7BAPI_KEY%7D"# thsi url is wrong
response = requests.get(url)
print(response.status_code)