"""
This project uses the pytest module to run all functional and unit tests.
The following module creates all the fixtures that pytest uses to run the tests

?the @pytest.fixture decorator tells pytest to use the following functions to
?get parameters for the different testing methods, scope="session" tells pytest
?to create the parameter when the testing session starts, scope="module" will
?recreate the parameter for each testing module

run this command to run all tests "pytest --cov=project --cov-report html:htmlcov"
saves coverage report in /htmlcov folder
"""
from models import DB
from config.application_factory import create_app
from os.path import exists
from os import remove
import pytest


@pytest.fixture(scope="session")
def test_client():
    """generates a test_client for the flask app with test configuration, creates
    a test database, and test secret code and returns the client

    Yields:
        Iterator[object]: flask test_client object
    """
    if exists("test_database.db"):
        remove("test_database.db")
    app = create_app("config_test.py")
    if not exists("test_database.db"):
        DB.create_all(app=app)

    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


class TestUser:
    def __init__(
        self, password1: str, password2: str, email: str, username: str
    ) -> None:
        self.password1 = password1
        self.password2 = password2
        self.email = email
        self.username = username
        self.access_token = None
        self.refresh_token = None

    def login(self, access_token: str, refresh_token: str) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token

    def refresh_access_token(self, access_token: str) -> None:
        self.access_token = access_token


@pytest.fixture(scope="module")
def test_users() -> list:
    """generates list of 7 test users, user index 0 has valid info, users with
    index 1-6 all have invalid characteristics

    Returns:
        list: list of TestUser objects
    """
    users = []
    for i in range(7):
        user = TestUser(
            f"password{i}", f"password{i}", f"email{i}@gmail.com", f"username{i}"
        )
        users.append(user)

    users[1].email = users[0].email  # !same email as user 0
    users[2].username = users[0].username  # !same username as user 0
    users[3].password1 = "incorrect password"  # !passwords don't match
    users[4].username = "a"  # !username too short
    users[5].password1 = "as"  # !password too short
    users[5].password2 = "as"  # !password too short
    users[6].email = "as"  # !email too short

    return users


class TestStock:
    def __init__(
        self, ticker: str, number_of_shares: float, cost_per_share: float
    ) -> None:
        self.ticker = ticker
        self.number_of_shares = number_of_shares
        self.cost_per_share = cost_per_share


@pytest.fixture(scope="module")
def test_stocks() -> list:
    """generates list of 10 test stocks with real tickers

    Returns:
        list: list of TestStock objects
    """
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
    def __init__(
        self, symbol: str, number_of_coins: float, cost_per_coin: float
    ) -> None:
        self.symbol = symbol
        self.number_of_coins = number_of_coins
        self.cost_per_coin = cost_per_coin


@pytest.fixture(scope="module")
def test_cryptos() -> list:
    """generates list of 10 test cryptos with real symbols

    Returns:
        list: list of TestCrypto objects
    """
    symbols = ["BTC", "ETH", "XLR", "DOGE", "HNT", "SHIB", "USDT", "ADA", "USDC", "BCH"]
    cryptos = []
    for i in range(len(symbols)):
        temp = TestCrypto(
            symbol=symbols[i], number_of_coins=i + 10, cost_per_coin=i * 20
        )
        cryptos.append(temp)

    return cryptos
