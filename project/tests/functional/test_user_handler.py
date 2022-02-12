import time


class TestUser:
    def test_delete_user(self, test_client: object, test_users: list) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a DELETE request is sent to '/user/delete'
        THEN check that user is deleted
        """
        # try to register user 0
        json = test_users[0].register_info()
        response = test_client.post("/user", json=json)

        # login user 0
        json = test_users[0].login_info()
        response = test_client.put("/user", json=json)

        # delete user 0
        json = {"access_token": response.json.get("access_token", {})}
        response = test_client.delete("/user/delete", json=json)
        assert b"user deleted successfully" in response.data

    def test_delete_already_deleted_user(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a DELETE request is sent to '/user/delete'
        THEN check that user does not exist
        """
        # try to register user 0
        json = test_users[0].register_info()
        response = test_client.post("/user", json=json)

        # login user 0
        json = test_users[0].login_info()
        response = test_client.put("/user", json=json)

        # delete user 0
        json = {"access_token": response.json.get("access_token", {})}
        response = test_client.delete("/user/delete", json=json)

        # try to delete deleted user, does not revoke access/refresh tokens
        response = test_client.delete("/user/delete", json=json)
        assert b"user does not exist" in response.data

    def test_deleted_user_accessing_login(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a PUT request is sent to '/user'
        THEN check that user cannot be logged in, because they have been deleted
        """
        # login user 0
        json = test_users[0].login_info()
        response = test_client.put("/user", json=json)

        assert b"Email not found" in response.data
        assert response.status_code == 404

    def test_register_user(self, test_client: object, test_users: list) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a POST request is sent to '/user'
        THEN check that user was created
        """
        json = test_users[0].register_info()
        response = test_client.post("/user", json=json)
        assert b"the user has been created" in response.data
        assert response.status_code == 200

    def test_register_user_email_taken(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a POST request is sent to '/user'
        THEN check that already in database
        """
        json = test_users[1].register_info()
        response = test_client.post("/user", json=json)
        assert b"Email is already in use" in response.data
        assert response.status_code == 409

    def test_register_user_username_taken(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a POST request is sent to '/user'
        THEN check that username already in database
        """
        json = test_users[2].register_info()
        response = test_client.post("/user", json=json)
        assert b"Username is already in use" in response.data
        assert response.status_code == 409

    def test_register_user_password_not_matching(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a POST request is sent to '/user'
        THEN check that passwords don't match
        """
        json = test_users[3].register_info()
        response = test_client.post("/user", json=json)
        assert b"Passwords don't match" in response.data
        assert response.status_code == 400

    def test_register_user_short_username(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a POST request is sent to '/user'
        THEN check that username too short
        """
        json = test_users[4].register_info()
        response = test_client.post("/user", json=json)
        assert b"Username is too short" in response.data
        assert response.status_code == 400

    def test_register_user_short_password(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a POST request is sent to '/user'
        THEN check that password too short
        """
        json = test_users[5].register_info()
        response = test_client.post("/user", json=json)
        assert b"Password is too short" in response.data
        assert response.status_code == 400

    def test_register_user_bad_email(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a POST request is sent to '/user'
        THEN check that email is invalid
        """
        json = test_users[6].register_info()
        response = test_client.post("/user", json=json)
        assert b"Email is invalid" in response.data
        assert response.status_code == 400

    def test_login_user_valid_email_and_password(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a PUT request is sent to '/user'
        THEN check that user is logged in
        """
        user = test_users[0]
        json = user.login_info()
        response = test_client.put("/user", json=json)
        assert b"successfully logged in" in response.data
        assert response.status_code == 200

    def test_login_user_invalid_email(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a PUT request is sent to '/user'
        THEN check that email not in database
        """
        json = test_users[0].login_info()
        json["email"] = test_users[2].email
        response = test_client.put("/user", json=json)
        assert b"Email not found" in response.data
        assert response.status_code == 404

    def test_login_user_invalid_password(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a PUT request is sent to '/user'
        THEN check that password is incorrect
        """
        json = test_users[0].login_info()
        json["password"] = test_users[1].password1
        response = test_client.put("/user", json=json)
        assert b"Password is incorrect" in response.data
        assert response.status_code == 400

    def test_logout_logged_in_user(self, test_client: object, test_users: list) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a DELETE request is sent to '/user'
        THEN check that user is logged out
        """
        user = test_users[0]
        json = user.login_info()
        response = test_client.put("/user", json=json)
        user.login(
            access_token=response.json.get("access_token", {}),
            refresh_token=response.json.get("refresh_token", {}),
        )
        json = test_users[0].tokens()
        response = test_client.delete("/user", json=json)
        assert b"user logged out" in response.data
        assert response.status_code == 200

    def test_refresh_access_token(self, test_client: object, test_users: list) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a PUT request is sent to '/user/refresh'
        THEN check that an access_token(refresh gives stale tokens) has been granted
        """
        json = test_users[0].tokens()
        response = test_client.put("/user/refresh", json=json)
        test_users[0].refresh_access_token(response.json.get("access_token", {}))

        assert b"access_token" in response.data
        assert response.status_code == 200

    def test_logout_user_with_stale_access_token(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a DELETE request is sent to '/user'
        THEN check that user has been logged out
        """
        json = test_users[0].tokens()
        response = test_client.delete("/user", json=json)
        assert b"user logged out" in response.data
        assert response.status_code == 200

    def test_deleted_user_accessing_refresh_url(
        self, test_client: object, test_users: list
    ) -> None:
        """
        GIVEN a flask test_client and test_users
        WHEN a PUT request is sent to '/user/refresh'
        THEN check that access_token cannot be refresh, because they have been deleted
        """
        user = test_users[0]

        # try to register user 0
        json = test_users[0].register_info()
        response = test_client.post("/user", json=json)

        # login user 0
        json = test_users[0].login_info()
        response = test_client.put("/user", json=json)
        user.login(
            access_token=response.json.get("access_token", {}),
            refresh_token=response.json.get("refresh_token", {}),
        )

        # delete user 0
        json = user.tokens()
        response = test_client.delete("/user/delete", json=json)

        # try to refresh access_token
        response = test_client.put("/user/refresh", json=json)

        assert b"user does not exist" in response.data
        assert response.status_code == 404
