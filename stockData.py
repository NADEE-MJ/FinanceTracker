import requests

base = 'https://www.alphavantage.co/'
f = open('AlphaVantageAPIKey.txt', 'r')
key = f.readline()
f.close()

#run main to create alpha vantage api key file and test it out
def createKeyFile():
    key = input("Enter alpha vantage api key: ")
    f = open('AlphaVantageAPIKey.txt', 'w')
    f.write(key)
    f.close()

def getCurrentStockPrice(ticker):
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': ticker,
        'datatype': 'json',
        'apikey': key
    }

    response = requests.get(base + 'query', params=params)
    stockPrice = response.json().get('Global Quote', {}).get('05. price', {})

    return float(stockPrice)

if __name__ == "__main__":
    createKeyFile()
    print(getCurrentStockPrice('SPY'))