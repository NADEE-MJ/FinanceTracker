"""
This file is similar to unit testing, actually might try to make a unit test file later
comment out parts of the code to test different parts of the api, certain parts rely on other parts
"""

import requests

base = "http://localhost:5000/"

#creating a couple users, stocks, and cryptos
class TestUser():
    def __init__(self, password1, password2, email, username):
        self.password1 = password1
        self.password2 = password2
        self.email = email
        self.username = username
        self.access_token = None
        self.refresh_token = None

    def login(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
    
    def refresh_access_token(self, access_token):
        self.access_token = access_token

class TestStock():
    def __init__(self, ticker, number_of_shares, cost_per_share):
        self.ticker = ticker
        self.number_of_shares = number_of_shares
        self.cost_per_share = cost_per_share

class TestCrypto():
    def __init__(self, symbol, number_of_coins, cost_per_coin):
        self.symbol = symbol
        self.number_of_coins = number_of_coins
        self.cost_per_coin = cost_per_coin

symbols = ['BTC', 'ETH', 'XLR', 'DOGE', 'HNT', 'SHIB', 'USDT', 'ADA', 'USDC', 'BCH']
cryptos=[]
for i in range(len(symbols)):
    temp= TestCrypto(symbol=symbols[i], number_of_coins=i+10, cost_per_coin=i*20)
    cryptos.append(temp)

tickers = ['aapl', 'msft', 't', 'intc', 'rklb', 'amd', 'tsla', 'nflx', 'rblx', 'spy']
stocks=[]
for i in range(len(tickers)):
    temp= TestStock(ticker=tickers[i], number_of_shares=i+10, cost_per_share=i*20)
    stocks.append(temp)

users = []
for i in range(11):
    user = TestUser(f'password{i}', f'password{i}', f'email{i}@email.com', f'username{i}')
    users.append(user)

"""
user creation tests
successful - 0, 2, 8-10
fails - 1, 3, 4-7
"""
users[1].email = users[0].email
users[3].username = users[2].username
users[4].password1 = 'incorrect password'
users[5].username = 'a'
users[6].password1 = 'as'
users[6].password2 = 'as'
users[7].email = 'as'

for user in users:
    params = {
        'email': user.email,
        'username': user.username,
        'password1': user.password1,
        'password2': user.password2
    }
    response = requests.post(base + 'user', json=params)
    print(response.json())
    

"""
user login testing
"""
success = [0, 2, 8, 9, 10]
users[0].email = 'asdfasdfasdf'
users[2].password1 = 'asdfasdfasdf'

for value in success:
    user = users[value]
    params = {
        'email': user.email,
        'password': user.password1
    }
    response = requests.put(base + 'user', json=params)
    print(response.json())
    data = {
        'access_token': response.json().get('access_token', {}),
        'refresh_token': response.json().get('refresh_token', {})
    }
    user.login(data['access_token'], data['refresh_token'])

"""
accesing required fresh page with fresh access_token

/crypto, /stock post, patch and delete require fresh access_token
"""
##################################
#stock model testing
logged_in = [8, 9, 10]

#/stock post requests
for user in logged_in:
    for i in range(user):
        params = {
            'ticker': stocks[i].ticker,
            'number_of_shares': stocks[i].number_of_shares,
            'cost_per_share': stocks[i].cost_per_share,
            'access_token': users[user].access_token
        }

        response = requests.post(base + 'stock', json=params)
        print(response.json())

#/stock patch requests
for user in logged_in:
    for i in range(user - 5):
        params = {
            'ticker': stocks[i].ticker,
            'new_number_of_shares': stocks[i].number_of_shares + 20,
            'access_token': users[user].access_token
        }

        response = requests.patch(base + 'stock', json=params)
        print(response.json())

#/stock delete requests
for user in logged_in:
    for i in range(3):
        params = {
            'ticker': stocks[i].ticker,
            'access_token': users[user].access_token
        }

        response = requests.delete(base + 'stock', json=params)
        print(response.json())

# /stock post requests for stocks user already owns
for user in logged_in:
    for i in range(6, user):
        params = {
            'ticker': stocks[i].ticker,
            'number_of_shares': stocks[i].number_of_shares,
            'cost_per_share': stocks[i].cost_per_share,
            'access_token': users[user].access_token
        }

        response = requests.post(base + 'stock', json=params)
        print(response.json())

#/stock patch requests for stocks that dont exist
for user in logged_in:
    for i in range(2):
        params = {
            'ticker': stocks[i].ticker,
            'new_number_of_shares': stocks[i].number_of_shares + 20,
            'access_token': users[user].access_token
        }

        response = requests.patch(base + 'stock', json=params)
        print(response.json())

#/stock delete requests for stocks that dont exist for user
for user in logged_in:
    for i in range(2):
        params = {
            'ticker': stocks[i].ticker,
            'access_token': users[user].access_token
        }

        response = requests.delete(base + 'stock', json=params)
        print(response.json())


############################################
#crypto model testing

#/crypto post requests
for user in logged_in:
    for i in range(user):
        params = {
            'symbol': cryptos[i].symbol,
            'number_of_coins': cryptos[i].number_of_coins,
            'cost_per_coin': cryptos[i].cost_per_coin,
            'access_token': users[user].access_token
        }

        response = requests.post(base + 'crypto', json=params)
        print(response.json())

#/crypto patch requests
for user in logged_in:
    for i in range(user - 5):
        params = {
            'symbol': cryptos[i].symbol,
            'new_number_of_coins': cryptos[i].number_of_coins + 20,
            'access_token': users[user].access_token
        }

        response = requests.patch(base + 'crypto', json=params)
        print(response.json())

#/crypto delete requests
for user in logged_in:
    for i in range(3):
        params = {
            'symbol': cryptos[i].symbol,
            'access_token': users[user].access_token
        }

        response = requests.delete(base + 'crypto', json=params)
        print(response.json())

#/crypto post requests for cryptos user already owns
for user in logged_in:
    for i in range(6, user):
        params = {
            'symbol': cryptos[i].symbol,
            'number_of_coins': cryptos[i].number_of_coins,
            'cost_per_coin': cryptos[i].cost_per_coin,
            'access_token': users[user].access_token
        }

        response = requests.post(base + 'crypto', json=params)
        print(response.json())

#/crypto patch requests for cryptos that dont exist for user
for user in logged_in:
    for i in range(2):
        params = {
            'symbol': cryptos[i].symbol,
            'new_number_of_coins': cryptos[i].number_of_coins + 20,
            'access_token': users[user].access_token
        }

        response = requests.patch(base + 'crypto', json=params)
        print(response.json())

#/crypto delete requests for cryptos that dont exist for user
for user in logged_in:
    for i in range(2):
        params = {
            'symbol': cryptos[i].symbol,
            'access_token': users[user].access_token
        }

        response = requests.delete(base + 'crypto', json=params)
        print(response.json())


"""
accessing page without an access token, when it is required
should say missing access_token key
"""
params = {
    'ticker': stocks[0].ticker,
    'number_of_shares': stocks[0].number_of_shares,
    'cost_per_share': stocks[0].cost_per_share
}
response = requests.get(base + 'stocks', json=params)
print(response.json())

"""
accessing page with an invalid access token
"""
params = {
    'ticker': stocks[0].ticker,
    'number_of_shares': stocks[0].number_of_shares,
    'cost_per_share': stocks[0].cost_per_share,
    'access_token': '4'
}
#not enough segments
response = requests.get(base + 'stocks', json=params)
print(response.json())

#invalid header padding
params['access_token'] = '4.4.4'
response = requests.get(base + 'stocks', json=params)
print(response.json())

#invalid payload padding
params['access_token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.4.4'
response = requests.get(base + 'stocks', json=params)
print(response.json())

#invalid crypto padding
params['access_token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQzNTY3MzczLCJqdGkiOiJhNj.4'
response = requests.get(base + 'stocks', json=params)
print(response.json())

#invalid payload string
params['access_token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQzNTY3MzczLCJqdGkiOiJhNj.s4sv-QqJhVq4cfu2cmhtB5X6P-i8ZyqEbUoKT94GswU'
response = requests.get(base + 'stocks', json=params)
print(response.json())

#should give signature verification failed 
params['access_token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQzNTY3NTk1LCJqdGkiOiIzMDExZTQzOC0zN2YyLTRmMTEtOGQ0Yy1mYjYxNGE4ZjJmYTUiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidXNlcm5hbWUzMCIsIm5iZiI6MTY0MzU2NzU5NSwiZXhwIjoxNjQzNTY5Mzk1fQ.lB0eR_azUVlrvYH92cWBT3CKJWKejzrIVP2y31_9MTk'
response = requests.get(base + 'stocks', json=params)
print(response.json())

"""
accesing no fresh requirements pages with fresh access_token

/cryptos, /crypto, /stock, /stocks get requests do not require fresh access tokens
"""
for user in logged_in:
    params = {
        'access_token': users[user].access_token
    }
    response = requests.get(base + 'stocks', json=params)
    print(response.json())
    response = requests.get(base + 'cryptos', json=params)
    print(response.json())
    for i in range(len(stocks)):
        params = {
            'ticker': stocks[i].ticker,
            'access_token': users[user].access_token
        }
        response = requests.get(base + 'stock', json=params)
        print(response.json())
    for i in range(len(cryptos)):
        params = {
            'symbol': cryptos[i].symbol,
            'access_token': users[user].access_token
        }
        response = requests.get(base + 'crypto', json=params)
        print(response.json())

#testing stocks and cryptos paths for a user with no crypto or stocks in database
#login user 0
user = users[0]
user.email = 'email0@email.com'
params = {
    'email': user.email,
    'password': user.password1
}
response = requests.put(base + 'user', json=params)
print(response.json())
data = {
    'access_token': response.json().get('access_token', {}),
    'refresh_token': response.json().get('refresh_token', {})
}
user.login(data['access_token'], data['refresh_token'])

params = {
    'access_token': user.access_token
}
response = requests.get(base + 'stocks', json=params)
print(response.json())
response = requests.get(base + 'cryptos', json=params)
print(response.json())
    
"""
log out users with fresh access_token
"""
for user in logged_in:
    params = {
        'access_token': users[user].access_token
    }
    response = requests.delete(base + 'user', json=params)
    print(response.json())

"""
log out users who already logged out
accessing page with revoked access_token
"""
for user in logged_in:
    params = {
        'access_token': users[user].access_token
    }
    response = requests.delete(base + 'user', json=params)
    print(response.json())

"""
/user/refresh - refresh access token, gives stale access_token, need valid refresh_token
"""
for user in logged_in:
    params = {
        'refresh_token': users[user].refresh_token
    }
    response = requests.put(base + 'user/refresh', json=params)
    print(response.json())
    users[user].refresh_access_token(response.json().get('access_token', {}))

"""
accessing required fresh page with unfresh access_token
"""
for user in logged_in:
    for i in range(3):
        params = {
            'ticker': stocks[i].ticker,
            'number_of_shares': stocks[i].number_of_shares,
            'cost_per_share': stocks[i].cost_per_share,
            'access_token': users[user].access_token
        }

        response = requests.delete(base + 'stock', json=params)
        print(response.json())
        response = requests.delete(base + 'crypto', json=params)
        print(response.json())

"""
accesing no requirements pages with stale access_token

/cryptos, /crypto, /stock, /stocks get requests do not require fresh access tokens
"""
for user in logged_in:
    params = {
        'access_token': users[user].access_token
    }
    response = requests.get(base + 'stocks', json=params)
    print(response.json())
    response = requests.get(base + 'cryptos', json=params)
    print(response.json())

"""
log out users with stale access_token
"""
for user in logged_in:
    params = {
        'access_token': users[user].access_token
    }
    response = requests.delete(base + 'user', json=params)
    print(response.json())