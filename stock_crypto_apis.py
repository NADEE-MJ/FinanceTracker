import requests
import yfinance as yf

base = 'https://www.alphavantage.co/'
f = open('AlphaVantageAPIKey.txt', 'r')
key = f.readline()
f.close()

#run file to create alpha vantage api key file and test it out
def createKeyFile():
    key = input("Enter alpha vantage api key: ")
    f = open('AlphaVantageAPIKey.txt', 'w')
    f.write(key)
    f.close()

def get_current_stock_price(ticker):
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': ticker,
        'datatype': 'json',
        'apikey': key
    }

    response = requests.get(base + 'query', params=params)
    if response.status_code != 200:
        stockPrice = response.json().get('Global Quote', {}).get('05. price', {})
        return float(stockPrice)
    else:
        stock_price = yf.Ticker(ticker).info.get('regularMarketPrice', {})
        return stock_price


if __name__ == "__main__":
    createKeyFile()
    print(get_current_stock_price('SPY'))