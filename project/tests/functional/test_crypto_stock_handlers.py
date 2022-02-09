from test_user_handler import set_json_register


class TestStocksAndCryptos:
    def test_get_stocks_user_owns_none(self, test_client, test_users):
        # register user
        json = set_json_register(0, test_users)
        response = test_client.post("/user", json=json)

        json = get_access_token(test_client, test_users[0])
        response = test_client.get("/stocks", json=json)
        assert b"[]" in response.data
        assert response.status_code == 200

    def test_get_cryptos_user_owns_none(self, test_client, test_users):
        json = get_access_token(test_client, test_users[0])
        response = test_client.get("/cryptos", json=json)
        assert b"[]" in response.data
        assert response.status_code == 200

    def test_get_cryptos(self, test_client, test_users, test_cryptos):
        json = get_access_token(test_client, test_users[0])
        json["symbol"] = test_cryptos[0].symbol
        json["number_of_coins"] = test_cryptos[0].number_of_coins
        json["cost_per_coin"] = test_cryptos[0].cost_per_coin

        response = test_client.post("/crypto", json=json)

        response = test_client.get("/cryptos", json=json)
        assert b"symbol" in response.data
        assert response.status_code == 200

        response = test_client.delete("/crypto", json=json)

    def test_get_stocks(self, test_client, test_users, test_stocks):
        json = get_access_token(test_client, test_users[0])
        json["ticker"] = test_stocks[0].ticker
        json["number_of_shares"] = test_stocks[0].number_of_shares
        json["cost_per_share"] = test_stocks[0].cost_per_share

        response = test_client.post("/stock", json=json)

        response = test_client.get("/stocks", json=json)
        assert b"ticker" in response.data
        assert response.status_code == 200

        response = test_client.delete("/stock", json=json)


class TestStock:
    def test_add_stock(self, test_client, test_users, test_stocks):
        json = get_access_token(test_client, test_users[0])
        # add first 5 test stocks to user 0
        for i in range(5):
            json["ticker"] = test_stocks[i].ticker
            json["number_of_shares"] = test_stocks[i].number_of_shares
            json["cost_per_share"] = test_stocks[i].cost_per_share

            response = test_client.post("/stock", json=json)
            assert b"ticker" in response.data
            assert response.status_code == 201

    def test_add_stock_user_already_owns(self, test_client, test_users, test_stocks):
        json = get_access_token(test_client, test_users[0])
        # add first 5 test stocks to user 0
        for i in range(5):
            json["ticker"] = test_stocks[i].ticker
            json["number_of_shares"] = test_stocks[i].number_of_shares
            json["cost_per_share"] = test_stocks[i].cost_per_share

            response = test_client.post("/stock", json=json)
            assert b"user already owns that stock" in response.data
            assert response.status_code == 400

    def test_edit_stock(self, test_client, test_users, test_stocks):
        json = get_access_token(test_client, test_users[0])
        # add first 5 test stocks to user 0
        for i in range(5):
            json["ticker"] = test_stocks[i].ticker
            json["new_number_of_shares"] = test_stocks[i].number_of_shares + 10

            response = test_client.patch("/stock", json=json)
            assert b"ticker" in response.data
            assert response.status_code == 200

    def test_edit_stock_user_does_not_own(self, test_client, test_users, test_stocks):
        json = get_access_token(test_client, test_users[0])
        # add first 5 test stocks to user 0
        for i in range(5, 10):
            json["ticker"] = test_stocks[i].ticker
            json["new_number_of_shares"] = test_stocks[i].number_of_shares + 10

            response = test_client.patch("/stock", json=json)
            assert b"user does not own that stock" in response.data
            assert response.status_code == 404

    def test_delete_stock(self, test_client, test_users, test_stocks):
        json = get_access_token(test_client, test_users[0])
        # delete first 2 test stocks for user 0
        for i in range(2):
            json["ticker"] = test_stocks[i].ticker

            response = test_client.delete("/stock", json=json)
            assert b"successfully deleted" in response.data
            assert response.status_code == 200

    def test_delete_stock_user_does_not_own(self, test_client, test_users, test_stocks):
        json = get_access_token(test_client, test_users[0])
        # delete first 2 test stocks for user 0
        for i in range(2):
            json["ticker"] = test_stocks[i].ticker

            response = test_client.delete("/stock", json=json)
            assert b"user does not own that stock" in response.data
            assert response.status_code == 404


class TestCrypto:
    def test_add_crypto(self, test_client, test_users, test_cryptos):
        json = get_access_token(test_client, test_users[0])
        # add first 5 test cryptos to user 0
        for i in range(5):
            json["symbol"] = test_cryptos[i].symbol
            json["number_of_coins"] = test_cryptos[i].number_of_coins
            json["cost_per_coin"] = test_cryptos[i].cost_per_coin

            response = test_client.post("/crypto", json=json)
            assert b"symbol" in response.data
            assert response.status_code == 201

    def test_add_crypto_user_already_owns(self, test_client, test_users, test_cryptos):
        json = get_access_token(test_client, test_users[0])
        # add first 5 test cryptos to user 0
        for i in range(5):
            json["symbol"] = test_cryptos[i].symbol
            json["number_of_coins"] = test_cryptos[i].number_of_coins
            json["cost_per_coin"] = test_cryptos[i].cost_per_coin

            response = test_client.post("/crypto", json=json)
            assert b"user already owns that crypto" in response.data
            assert response.status_code == 400

    def test_edit_crypto(self, test_client, test_users, test_cryptos):
        json = get_access_token(test_client, test_users[0])
        # add first 5 test cryptos to user 0
        for i in range(5):
            json["symbol"] = test_cryptos[i].symbol
            json["new_number_of_coins"] = test_cryptos[i].number_of_coins + 10

            response = test_client.patch("/crypto", json=json)
            assert b"symbol" in response.data
            assert response.status_code == 200

    def test_edit_crypto_user_does_not_own(self, test_client, test_users, test_cryptos):
        json = get_access_token(test_client, test_users[0])
        # add first 5 test cryptos to user 0
        for i in range(5, 10):
            json["symbol"] = test_cryptos[i].symbol
            json["new_number_of_coins"] = test_cryptos[i].number_of_coins + 10

            response = test_client.patch("/crypto", json=json)
            assert b"user does not own that crypto" in response.data
            assert response.status_code == 404

    def test_delete_crypto(self, test_client, test_users, test_cryptos):
        json = get_access_token(test_client, test_users[0])
        # delete first 2 test cryptos for user 0
        for i in range(2):
            json["symbol"] = test_cryptos[i].symbol

            response = test_client.delete("/crypto", json=json)
            assert b"successfully deleted" in response.data
            assert response.status_code == 200

    def test_delete_crypto_user_does_not_own(
        self, test_client, test_users, test_cryptos
    ):
        json = get_access_token(test_client, test_users[0])
        # delete first 2 test cryptos for user 0
        for i in range(2):
            json["symbol"] = test_cryptos[i].symbol

            response = test_client.delete("/crypto", json=json)
            assert b"user does not own that crypto" in response.data
            assert response.status_code == 404


def get_access_token(client: object, user: object):
    json = {"email": user.email, "password": user.password1}
    response = client.put("/user", json=json)
    json = {"access_token": response.json.get("access_token", {})}

    return json
