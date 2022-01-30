from urllib.error import HTTPError
import requests
import yfinance as yf

base = 'https://www.alphavantage.co/'

def create_key_file():
    key = input('Enter alpha vantage api key: ')
    f = open('ALPHA_VANTAGE_API_KEY.txt', 'w')
    f.write(key)
    f.close()
    print('API key file created!')

try:
    f = open('ALPHA_VANTAGE_API_KEY.txt', 'r')
    key = f.readline()
    f.close()
except FileNotFoundError:
    create_key_file()

def get_current_stock_price(ticker):
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': ticker,
        'datatype': 'json',
        'apikey': key
    }

    try:
        response = requests.get(base + 'query', params=params)
    
        if response.status_code != 200:
            raise HTTPError 
        stock_price = response.json().get('Global Quote', {}).get('05. price', {})
        return float(stock_price)
    except HTTPError:
        stock_price = yf.Ticker(ticker).info.get('regularMarketPrice', {})
        return stock_price

if __name__ == '__main__':
    print(get_current_stock_price('SPY'))