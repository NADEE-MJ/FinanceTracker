class TestStocksAndCryptos:
    def test_get_stocks_user_owns_none(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)

        response = test_client.get("/stocks", json=user.tokens())

        assert b"[]" in response.data
        assert response.status_code == 200

    def test_get_stocks(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        stock = test_stocks[0]
        json = user.tokens()

        json["ticker"] = stock.ticker
        json["number_of_shares"] = stock.number_of_shares
        json["cost_per_share"] = stock.cost_per_share

        # add stock
        response = test_client.post("/stock", json=json)

        # check what stocks are owned
        response = test_client.get("/stocks", json=json)

        assert b"ticker" in response.data
        assert response.status_code == 200

        # delete stock for next test
        response = test_client.delete("/stock", json=json)

    def test_get_stocks_user_does_not_exist(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        user.delete_user(test_client)

        response = test_client.get("/stocks", json=user.tokens())

        assert b"user does not exist" in response.data
        assert response.status_code == 404

    def test_get_cryptos_user_owns_none(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)

        response = test_client.get("/cryptos", json=user.tokens())

        assert b"[]" in response.data
        assert response.status_code == 200

    def test_get_cryptos(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        crypto = test_cryptos[0]
        json = user.tokens()

        json["symbol"] = crypto.symbol
        json["number_of_coins"] = crypto.number_of_coins
        json["cost_per_coin"] = crypto.cost_per_coin

        # add crypto
        response = test_client.post("/crypto", json=json)

        # check what cryptos are owned
        response = test_client.get("/cryptos", json=json)

        assert b"symbol" in response.data
        assert response.status_code == 200

        # delete crypto for next test
        response = test_client.delete("/crypto", json=json)

    def test_get_cryptos_user_does_not_exist(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        user.delete_user(test_client)

        response = test_client.get("/cryptos", json=user.tokens())

        assert b"user does not exist" in response.data
        assert response.status_code == 404
