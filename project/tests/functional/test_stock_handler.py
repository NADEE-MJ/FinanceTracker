class TestStock:
    def test_add_stock(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        json = user.tokens()

        for i in range(5):
            json["ticker"] = test_stocks[i].ticker
            json["number_of_shares"] = test_stocks[i].number_of_shares
            json["cost_per_share"] = test_stocks[i].cost_per_share

            response = test_client.post("/stock", json=json)

            assert b"ticker" in response.data
            assert response.status_code == 201

    def test_add_stock_user_already_owns(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()

        for i in range(5):
            json["ticker"] = test_stocks[i].ticker
            json["number_of_shares"] = test_stocks[i].number_of_shares
            json["cost_per_share"] = test_stocks[i].cost_per_share

            response = test_client.post("/stock", json=json)

            assert b"user already owns that stock" in response.data
            assert response.status_code == 400

    def test_add_stock_to_deleted_user(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()
        user.delete_user(test_client)

        for i in range(5):
            json["ticker"] = test_stocks[i].ticker
            json["number_of_shares"] = test_stocks[i].number_of_shares
            json["cost_per_share"] = test_stocks[i].cost_per_share

            response = test_client.post("/stock", json=json)

            assert b"user does not exist" in response.data
            assert response.status_code == 404

    def test_get_stock(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        json = user.tokens()

        for i in range(5):
            json["ticker"] = test_stocks[i].ticker
            json["number_of_shares"] = test_stocks[i].number_of_shares
            json["cost_per_share"] = test_stocks[i].cost_per_share

            test_client.post("/stock", json=json)

            response = test_client.get("/stock", json=json)

            assert b"ticker" in response.data
            assert response.status_code == 200

    def test_get_stock_user_does_not_own(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()

        for i in range(5, 10):
            json["ticker"] = test_stocks[i].ticker

            response = test_client.get("/stock", json=json)

            assert b"stock not found" in response.data
            assert response.status_code == 404

    def test_get_stock_for_deleted_user(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()
        user.delete_user(test_client)

        for i in range(5, 10):
            json["ticker"] = test_stocks[i].ticker

            response = test_client.get("/stock", json=json)

            assert b"user does not exist" in response.data
            assert response.status_code == 404

    def test_edit_stock(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        json = user.tokens()

        for i in range(5):
            json["ticker"] = test_stocks[i].ticker
            json["number_of_shares"] = test_stocks[i].number_of_shares
            json["cost_per_share"] = test_stocks[i].cost_per_share

            test_client.post("/stock", json=json)

            json["new_number_of_shares"] = test_stocks[i].number_of_shares + 10

            response = test_client.patch("/stock", json=json)
            assert b"ticker" in response.data
            assert response.status_code == 200

    def test_edit_stock_user_does_not_own(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()

        for i in range(5, 10):
            json["ticker"] = test_stocks[i].ticker
            json["new_number_of_shares"] = test_stocks[i].number_of_shares + 10

            response = test_client.patch("/stock", json=json)
            assert b"user does not own that stock" in response.data
            assert response.status_code == 404

    def test_edit_stock_for_deleted_user(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()
        user.delete_user(test_client)

        for i in range(5):
            json["ticker"] = test_stocks[i].ticker
            json["new_number_of_shares"] = test_stocks[i].number_of_shares + 10

            response = test_client.patch("/stock", json=json)
            assert b"user does not exist" in response.data
            assert response.status_code == 404

    def test_delete_stock(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        json = user.tokens()

        for i in range(2):
            json["ticker"] = test_stocks[i].ticker
            json["number_of_shares"] = test_stocks[i].number_of_shares
            json["cost_per_share"] = test_stocks[i].cost_per_share

            test_client.post("/stock", json=json)

            response = test_client.delete("/stock", json=json)
            assert b"successfully deleted" in response.data
            assert response.status_code == 200

    def test_delete_stock_user_does_not_own(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()

        for i in range(2):
            json["ticker"] = test_stocks[i].ticker

            response = test_client.delete("/stock", json=json)
            assert b"user does not own that stock" in response.data
            assert response.status_code == 404

    def test_delete_stock_user_does_not_exist(
        self, test_client: object, test_users: list, test_stocks: list
    ) -> None:
        user = test_users[0]
        json = user.tokens()
        user.delete_user(test_client)

        for i in range(2):
            json["ticker"] = test_stocks[i].ticker

            response = test_client.delete("/stock", json=json)
            assert b"user does not exist" in response.data
            assert response.status_code == 404
