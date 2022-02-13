from models import TokenBlocklist, UserModel, StockModel, CryptoModel, add_to_database
from datetime import datetime, timezone


class TestTokens:
    def test_create_blocked_token(self) -> None:
        jti = "test"
        now = datetime.now(timezone.utc)
        token = TokenBlocklist(jti=jti, revoked_at=now)

        assert token.jti == jti
        assert token.revoked_at == now


class TestUserModel:
    def test_create_user(self, test_user_model: object) -> None:
        user = test_user_model

        assert user.email == "pytest@test.com"
        assert user.username == "testusername"
        assert user.password == "testpassword"

    def test_repr_method(self, test_user_model: object) -> None:
        user = test_user_model
        repr_string = user.__repr__()

        assert "User" in repr_string

    def test_fresh_login(self, test_user_model: object) -> None:
        user = test_user_model

        tokens = user.fresh_login()

        assert "access_token" in tokens

    def test_stale_login(self, test_user_model: object) -> None:
        user = test_user_model

        token = user.stale_login()

        assert "access_token" in token


class TestStockModel:
    def test_create_stock(self, test_stock_model: tuple) -> None:
        stock, owner_id = test_stock_model

        assert stock.ticker == "test"
        assert stock.number_of_shares == 100
        assert stock.cost_per_share == 100
        assert stock.owner_id == owner_id

    def test_repr_method(self, test_stock_model: tuple) -> None:
        stock = test_stock_model[0]

        repr_string = stock.__repr__()

        assert "Stock" in repr_string

    def test_update_shares(self, test_stock_model: tuple) -> None:
        email = "pytest2@test.com"
        username = "testusername2"
        password = "testpassword"

        user = UserModel(email=email, username=username, password=password)
        add_to_database(user)
        user_from_db = UserModel.query.filter_by(username=username).first()

        stock = test_stock_model[0]
        stock.owner_id = user_from_db.id
        add_to_database(stock)

        new_shares = 5

        stock.update_shares(new_shares)
        stock_from_db = StockModel.query.filter_by(owner_id=user_from_db.id).first()

        assert stock_from_db.number_of_shares == new_shares


class TestCryptoModel:
    def test_create_crypto(self, test_crypto_model: tuple) -> None:
        crypto, owner_id = test_crypto_model

        assert crypto.symbol == "test"
        assert crypto.number_of_coins == 100
        assert crypto.cost_per_coin == 100
        assert crypto.owner_id == owner_id

    def test_repr_method(self, test_crypto_model: tuple) -> None:
        crypto = test_crypto_model[0]

        repr_string = crypto.__repr__()

        assert "Crypto" in repr_string

    def test_update_coins(self, test_crypto_model: tuple) -> None:
        email = "pytest3@test.com"
        username = "testusername3"
        password = "testpassword"

        user = UserModel(email=email, username=username, password=password)
        add_to_database(user)
        user_from_db = UserModel.query.filter_by(username=username).first()

        crypto = test_crypto_model[0]
        crypto.owner_id = user_from_db.id
        add_to_database(crypto)

        new_coins = 5

        crypto.update_coins(new_coins)

        crypto_from_db = CryptoModel.query.filter_by(owner_id=user_from_db.id).first()

        assert crypto_from_db.number_of_coins == new_coins
