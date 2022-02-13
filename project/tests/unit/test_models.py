from models import TokenBlocklist, UserModel, StockModel, CryptoModel
from datetime import datetime, timezone


class TestTokens:
    def test_create_blocked_token(self):
        jti = "test"
        now = datetime.now(timezone.utc)
        token = TokenBlocklist(jti=jti, revoked_at=now)

        assert token.jti == jti
        assert token.revoked_at == now


class TestUserModel:
    def test_create_user(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)

        assert user.email == email
        assert user.username == username
        assert user.password == password

    def test_repr_method(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)
        repr_string = user.__repr__()

        assert "User" in repr_string

    def test_fresh_login(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)

        tokens = user.fresh_login()

        assert "access_token" in tokens

    def test_stale_login(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)

        token = user.stale_login()

        assert "access_token" in token


class TestStockModel:
    def test_create_stock(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)

        ticker = "test"
        number_of_shares = 100
        cost_per_share = 1000
        owner_id = user.id

        stock = StockModel(
            ticker=ticker,
            number_of_shares=number_of_shares,
            cost_per_share=cost_per_share,
            owner_id=owner_id,
        )

        assert stock.ticker == ticker
        assert stock.number_of_shares == number_of_shares
        assert stock.cost_per_share == cost_per_share
        assert stock.owner_id == owner_id

    def test_repr_method(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)

        ticker = "test"
        number_of_shares = 100
        cost_per_share = 1000
        owner_id = user.id

        stock = StockModel(
            ticker=ticker,
            number_of_shares=number_of_shares,
            cost_per_share=cost_per_share,
            owner_id=owner_id,
        )

        repr_string = stock.__repr__()

        assert "Stock" in repr_string

    def test_update_shares(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)

        ticker = "test"
        number_of_shares = 100
        cost_per_share = 1000
        owner_id = user.id

        stock = StockModel(
            ticker=ticker,
            number_of_shares=number_of_shares,
            cost_per_share=cost_per_share,
            owner_id=owner_id,
        )

        new_shares = 5

        stock.update_shares(new_shares)

        assert stock.number_of_shares == new_shares


class TestCryptoModel:
    def test_create_crypto(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)

        symbol = "test"
        number_of_coins = 100
        cost_per_coin = 1000
        owner_id = user.id

        crypto = CryptoModel(
            symbol=symbol,
            number_of_coins=number_of_coins,
            cost_per_coin=cost_per_coin,
            owner_id=owner_id,
        )

        assert crypto.symbol == symbol
        assert crypto.number_of_coins == number_of_coins
        assert crypto.cost_per_coin == cost_per_coin
        assert crypto.owner_id == owner_id

    def test_repr_method(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)

        symbol = "test"
        number_of_coins = 100
        cost_per_coin = 1000
        owner_id = user.id

        crypto = CryptoModel(
            symbol=symbol,
            number_of_coins=number_of_coins,
            cost_per_coin=cost_per_coin,
            owner_id=owner_id,
        )

        repr_string = crypto.__repr__()

        assert "Crypto" in repr_string

    def test_update_coins(self):
        email = "test@example.com"
        username = "test"
        password = "test"

        user = UserModel(email=email, username=username, password=password)

        symbol = "test"
        number_of_coins = 100
        cost_per_coin = 1000
        owner_id = user.id

        crypto = CryptoModel(
            symbol=symbol,
            number_of_coins=number_of_coins,
            cost_per_coin=cost_per_coin,
            owner_id=owner_id,
        )

        new_coins = 5

        crypto.update_coins(new_coins)

        assert crypto.number_of_coins == new_coins
