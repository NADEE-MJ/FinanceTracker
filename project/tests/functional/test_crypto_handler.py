class TestCrypto:
    def test_add_crypto(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        json = user.tokens()

        for i in range(5):
            json["symbol"] = test_cryptos[i].symbol
            json["number_of_coins"] = test_cryptos[i].number_of_coins
            json["cost_per_coin"] = test_cryptos[i].cost_per_coin

            response = test_client.post("/crypto", json=json)

            assert b"symbol" in response.data
            assert response.status_code == 201

    def test_add_crypto_user_already_owns(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()

        for i in range(5):
            json["symbol"] = test_cryptos[i].symbol
            json["number_of_coins"] = test_cryptos[i].number_of_coins
            json["cost_per_coin"] = test_cryptos[i].cost_per_coin

            response = test_client.post("/crypto", json=json)

            assert b"user already owns that crypto" in response.data
            assert response.status_code == 400

    def test_add_crypto_to_deleted_user(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()
        user.delete_user(test_client)

        for i in range(5):
            json["symbol"] = test_cryptos[i].symbol
            json["number_of_coins"] = test_cryptos[i].number_of_coins
            json["cost_per_coin"] = test_cryptos[i].cost_per_coin

            response = test_client.post("/crypto", json=json)

            assert b"user does not exist" in response.data
            assert response.status_code == 404

    def test_get_crypto(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        json = user.tokens()

        for i in range(5):
            json["symbol"] = test_cryptos[i].symbol
            json["number_of_coins"] = test_cryptos[i].number_of_coins
            json["cost_per_coin"] = test_cryptos[i].cost_per_coin

            test_client.post("/crypto", json=json)

            response = test_client.get("/crypto", json=json)

            assert b"symbol" in response.data
            assert response.status_code == 200

    def test_get_crypto_user_does_not_own(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()

        for i in range(5, 10):
            json["symbol"] = test_cryptos[i].symbol

            response = test_client.get("/crypto", json=json)

            assert b"crypto not found" in response.data
            assert response.status_code == 404

    def test_get_crypto_for_deleted_user(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()
        user.delete_user(test_client)

        for i in range(5, 10):
            json["symbol"] = test_cryptos[i].symbol

            response = test_client.get("/crypto", json=json)

            assert b"user does not exist" in response.data
            assert response.status_code == 404

    def test_edit_crypto(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        json = user.tokens()

        for i in range(5):
            json["symbol"] = test_cryptos[i].symbol
            json["number_of_coins"] = test_cryptos[i].number_of_coins
            json["cost_per_coin"] = test_cryptos[i].cost_per_coin

            test_client.post("/crypto", json=json)

            json["new_number_of_coins"] = test_cryptos[i].number_of_coins + 10

            response = test_client.patch("/crypto", json=json)
            assert b"symbol" in response.data
            assert response.status_code == 200

    def test_edit_crypto_user_does_not_own(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()

        for i in range(5, 10):
            json["symbol"] = test_cryptos[i].symbol
            json["new_number_of_coins"] = test_cryptos[i].number_of_coins + 10

            response = test_client.patch("/crypto", json=json)
            assert b"user does not own that crypto" in response.data
            assert response.status_code == 404

    def test_edit_crypto_for_deleted_user(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()
        user.delete_user(test_client)

        for i in range(5):
            json["symbol"] = test_cryptos[i].symbol
            json["new_number_of_coins"] = test_cryptos[i].number_of_coins + 10

            response = test_client.patch("/crypto", json=json)
            assert b"user does not exist" in response.data
            assert response.status_code == 404

    def test_delete_crypto(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        json = user.tokens()

        for i in range(2):
            json["symbol"] = test_cryptos[i].symbol
            json["number_of_coins"] = test_cryptos[i].number_of_coins
            json["cost_per_coin"] = test_cryptos[i].cost_per_coin

            test_client.post("/crypto", json=json)

            response = test_client.delete("/crypto", json=json)
            assert b"successfully deleted" in response.data
            assert response.status_code == 200

    def test_delete_crypto_user_does_not_own(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()

        for i in range(2):
            json["symbol"] = test_cryptos[i].symbol

            response = test_client.delete("/crypto", json=json)
            assert b"user does not own that crypto" in response.data
            assert response.status_code == 404

    def test_delete_crypto_user_does_not_exist(
        self, test_client: object, test_users: list, test_cryptos: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()
        user.delete_user(test_client)

        for i in range(2):
            json["symbol"] = test_cryptos[i].symbol

            response = test_client.delete("/crypto", json=json)
            assert b"user does not exist" in response.data
            assert response.status_code == 404
