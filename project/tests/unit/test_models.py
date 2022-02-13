from models import TokenBlocklist, UserModel, StockModel, CryptoModel
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
    def test_create_stock(self, test_stock_model: object) -> None:
        stock = test_stock_model[1]

        assert stock.ticker == "test"
        assert stock.number_of_shares == 100
        assert stock.cost_per_share == 100
        assert stock.owner_id == test_stock_model[0].id

    def test_repr_method(self, test_stock_model: object) -> None:
        stock = test_stock_model[1]

        repr_string = stock.__repr__()

        assert "Stock" in repr_string

    def test_update_shares(self, test_stock_model: object) -> None:
        stock = test_stock_model[1]

        new_shares = 5

        stock.update_shares(new_shares)

        assert stock.number_of_shares == new_shares


class TestCryptoModel:
    def test_create_crypto(self, test_crypto_model: object) -> None:
        crypto = test_crypto_model[1]

        assert crypto.symbol == "test"
        assert crypto.number_of_coins == 100
        assert crypto.cost_per_coin == 100
        assert crypto.owner_id == test_crypto_model[0].id

    def test_repr_method(self, test_crypto_model: object) -> None:
        crypto = test_crypto_model[1]

        repr_string = crypto.__repr__()

        assert "Crypto" in repr_string

    def test_update_coins(self, test_crypto_model: object) -> None:
        crypto = test_crypto_model[1]

        new_coins = 5

        crypto.update_coins(new_coins)

        assert crypto.number_of_coins == new_coins
