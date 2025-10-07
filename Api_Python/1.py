""" Api: Application Programmng Interface 
In simple Terms its set of rules and protocols That allow how different software
application can communicate and interact with each other..
"""
# api acts as bridge that easily exchange information and functionality

# Making Api requests inpython
#pip install requests
import requests
# import requests
import json
def get_stock_data():
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=demo"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        with open ('1.json','w') as j:
            json.dump(data,j,indent=4)
        last_refreshed = data["Meta Data"]["3. Last Refreshed"]
        price_open = data["Time Series (5min)"][last_refreshed]["1. open"]
        price_close = data["Time Series (5min)"][last_refreshed]["4. close"]
        # return price
        return price_open,price_close
    else:
        return None

price_open,price_close = get_stock_data()
symbol = "IBM"
if price_open is not None:
    print(f"{symbol}: {price_open}")
    if price_close is not None:
        print(f"{symbol}: {price_close}")
else:
    print("Failed to retrieve data.")


