from models import StockModel, db
from config.application_factory import create_app
from os.path import exists
import pytest


@pytest.fixture(scope="module")
def test_client():
    app = create_app("config_test.py")
    if not exists("test_database.db"):
        db.create_all(app=app)

    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


class FakeUser:
    def __init__(self, email: str, username: str, password1: str, password2: str):
        self.email = email
        self.username = username
        self.password1 = password1
        self.password2 = password2
        self.access_token = None
        self.refresh_token = None

    def save_tokens(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token


@pytest.fixture(scope="module")
def new_user():
    new_user = FakeUser(
        email="pytest@gmail.com",
        username="pytest",
        password1="pytestpass",
        password2="pytestpass",
    )
    return new_user


@pytest.fixture(scope="module")
def existing_user():
    pass


@pytest.fixture(scope="module")
def test_stock():
    return StockModel(
        ticker="aapl".upper(), number_of_shares=50, cost_per_share=20, owner=2
    )
