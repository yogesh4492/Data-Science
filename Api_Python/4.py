import requests

API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "d66ea8c899c4415d91f5301d8edc643d"

params = {
    "country": "us",
    "apiKey": API_KEY,
    "pageSize": 1
}

response = requests.get(API_URL, params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")