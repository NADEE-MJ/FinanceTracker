class TestUser:
    def test_delete_user(self, test_client: object, test_users: list[object]) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)

        # delete user
        response = test_client.delete("/user/delete", json=user.tokens())

        assert b"user deleted successfully" in response.data

    def test_delete_already_deleted_user(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        user.delete_user(test_client)

        # try to delete deleted user, does not revoke access/refresh tokens
        response = test_client.delete("/user/delete", json=user.tokens())

        assert b"user does not exist" in response.data

    def test_deleted_user_accessing_login(
        self, test_client: object, test_users: list[object]
    ) -> None:

        user = test_users[0]

        # login user
        response = test_client.put("/user", json=user.login_info())

        assert b"Email not found" in response.data
        assert response.status_code == 404

    def test_register_user(self, test_client: object, test_users: list[object]) -> None:
        user = test_users[0]
        response = test_client.post("/user", json=user.register_info())

        assert b"the user has been created" in response.data
        assert response.status_code == 200

    def test_register_user_email_taken(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[1]
        response = test_client.post("/user", json=user.register_info())

        assert b"Email is already in use" in response.data
        assert response.status_code == 409

    def test_register_user_username_taken(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[2]
        response = test_client.post("/user", json=user.register_info())

        assert b"Username is already in use" in response.data
        assert response.status_code == 409

    def test_register_user_password_not_matching(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[3]
        response = test_client.post("/user", json=user.register_info())

        assert b"Passwords don't match" in response.data
        assert response.status_code == 400

    def test_register_user_short_username(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[4]
        response = test_client.post("/user", json=user.register_info())

        assert b"Username is too short" in response.data
        assert response.status_code == 400

    def test_register_user_short_password(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[5]
        response = test_client.post("/user", json=user.register_info())

        assert b"Password is too short" in response.data
        assert response.status_code == 400

    def test_register_user_bad_email(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[6]
        response = test_client.post("/user", json=user.register_info())

        assert b"Email is invalid" in response.data
        assert response.status_code == 400

    def test_login_user_valid_email_and_password(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[0]
        response = test_client.put("/user", json=user.login_info())

        assert b"successfully logged in" in response.data
        assert response.status_code == 200

    def test_login_user_invalid_email(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[0]
        json = user.login_info()
        json["email"] = test_users[2].email
        response = test_client.put("/user", json=json)

        assert b"Email not found" in response.data
        assert response.status_code == 404

    def test_login_user_invalid_password(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[0]
        json = user.login_info()
        json["password"] = test_users[1].password1
        response = test_client.put("/user", json=json)

        assert b"Password is incorrect" in response.data
        assert response.status_code == 400

    def test_logout_logged_in_user(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[0]
        user.login(test_client)
        response = test_client.delete("/user", json=user.tokens())

        assert b"user logged out" in response.data
        assert response.status_code == 200

    def test_refresh_access_token(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[0]
        response = test_client.put("/user/refresh", json=user.tokens())

        assert b"access_token" in response.data
        assert response.status_code == 200

    def test_logout_user_with_stale_access_token(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[0]
        user.refresh_access_token(test_client)
        response = test_client.delete("/user", json=user.tokens())

        assert b"user logged out" in response.data
        assert response.status_code == 200

    def test_deleted_user_accessing_refresh_url(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[0]

        user.register(test_client)

        user.login(test_client)

        user.delete_user(test_client)

        # try to refresh access_token
        response = test_client.put("/user/refresh", json=user.tokens())

        assert b"user does not exist" in response.data
        assert response.status_code == 404
