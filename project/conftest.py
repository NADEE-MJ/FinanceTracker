from models import UserModel, StockModel, CryptoModel, add_to_database
from config import create_app, DB
from os.path import exists
from os import remove, path
from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def test_client():
    base_dir = Path(path.abspath(path.dirname(__file__)))
    parent_dir = base_dir.parent.absolute()
    if exists("test_database.db"):
        remove("test_database.db")
    app = create_app(path.join(parent_dir, "project/tests/config.py"))
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

    def register_info(self) -> dict:
        json = {
            "email": self.email,
            "username": self.username,
            "password1": self.password1,
            "password2": self.password2,
        }
        return json

    def register(self, client: object) -> None:
        client.post("/user", json=self.register_info())

    def login_info(self) -> dict:
        json = {"email": self.email, "password": self.password1}
        return json

    def login(self, client: object) -> None:
        response = client.put("/user", json=self.login_info())
        self.access_token = response.json.get("access_token", {})
        self.refresh_token = response.json.get("refresh_token", {})

    def logout(self, client: object) -> None:
        client.delete("/user", json=self.tokens())

    def delete_user(self, client: object) -> None:
        client.delete("/user/delete", json=self.tokens())

    def refresh_access_token(self, client: object) -> None:
        response = client.put("/user/refresh", json=self.tokens())
        self.access_token = response.json.get("access_token", {})

    def tokens(self) -> dict:
        json = {"access_token": self.access_token, "refresh_token": self.refresh_token}
        return json


# generates list of 7 test users, user index 0 has valid info, users with
# index 1-6 all have invalid characteristics
@pytest.fixture(scope="module")
def test_users() -> list:

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
    symbols = ["BTC", "ETH", "XLR", "DOGE", "HNT", "SHIB", "USDT", "ADA", "USDC", "BCH"]
    cryptos = []
    for i in range(len(symbols)):
        temp = TestCrypto(
            symbol=symbols[i], number_of_coins=i + 10, cost_per_coin=i * 20
        )
        cryptos.append(temp)

    return cryptos


@pytest.fixture(scope="function")
def test_user_model() -> object:
    email = "pytest@test.com"
    username = "testusername"
    password = "testpassword"

    user = UserModel(email=email, username=username, password=password)

    return user


@pytest.fixture(scope="function")
def test_stock_model() -> tuple:
    ticker = "test"
    number_of_shares = 100
    cost_per_share = 100
    owner_id = 1

    stock = StockModel(
        ticker=ticker,
        number_of_shares=number_of_shares,
        cost_per_share=cost_per_share,
        owner_id=owner_id,
    )

    return (stock, owner_id)


@pytest.fixture(scope="function")
def test_crypto_model() -> tuple:
    symbol = "test"
    number_of_coins = 100
    cost_per_coin = 100
    owner_id = 1

    crypto = CryptoModel(
        symbol=symbol,
        number_of_coins=number_of_coins,
        cost_per_coin=cost_per_coin,
        owner_id=owner_id,
    )

    return (crypto, owner_id)
