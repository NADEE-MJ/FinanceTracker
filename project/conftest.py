from models import db
from config.application_factory import create_app
from os.path import exists
from os import remove
import pytest


@pytest.fixture(scope="module")
def test_client():
    if exists("test_database.db"):
        remove("test_database.db")
    app = create_app("config_test.py")
    if not exists("test_database.db"):
        db.create_all(app=app)

    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


class TestUser:
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


@pytest.fixture(scope="module")
def test_users():
    users = []
    for i in range(8):
        user = TestUser(
            f"password{i}", f"password{i}", f"email{i}@email.com", f"username{i}"
        )
        users.append(user)

    # users 1-7 fail in different ways
    users[1].email = users[0].email
    users[2].username = users[0].username
    users[3].password1 = "incorrect password"
    users[4].username = "a"
    users[5].password1 = "as"
    users[5].password2 = "as"
    users[6].email = "as"

    return users


class TestStock:
    def __init__(self, ticker, number_of_shares, cost_per_share):
        self.ticker = ticker
        self.number_of_shares = number_of_shares
        self.cost_per_share = cost_per_share


@pytest.fixture(scope="module")
def test_stocks():
    tickers = [
        "aapl",
        "msft",
        "t",
        "intc",
        "rklb",
        "amd",
        "tsla",
        "nflx",
        "rblx",
        "spy",
    ]
    stocks = []
    for i in range(len(tickers)):
        temp = TestStock(
            ticker=tickers[i], number_of_shares=i + 10, cost_per_share=i * 20
        )
        stocks.append(temp)

    return stocks


class TestCrypto:
    def __init__(self, symbol, number_of_coins, cost_per_coin):
        self.symbol = symbol
        self.number_of_coins = number_of_coins
        self.cost_per_coin = cost_per_coin


@pytest.fixture(scope="module")
def test_cryptos():
    symbols = ["BTC", "ETH", "XLR", "DOGE", "HNT", "SHIB", "USDT", "ADA", "USDC", "BCH"]
    cryptos = []
    for i in range(len(symbols)):
        temp = TestCrypto(
            symbol=symbols[i], number_of_coins=i + 10, cost_per_coin=i * 20
        )
        cryptos.append(temp)

    return cryptos
