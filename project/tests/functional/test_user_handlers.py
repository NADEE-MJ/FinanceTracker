class TestUser:
    def test_delete_user(self, test_client, test_users):
        # register user
        json = set_json_register(0, test_users)
        response = test_client.post("/user", json=json)

        # login user
        json = {"email": test_users[0].email, "password": test_users[0].password1}
        response = test_client.put("/user", json=json)

        # delete user
        json = {"access_token": response.json.get("access_token", {})}
        response = test_client.delete("/user/delete", json=json)
        assert b"user deleted successfully" in response.data

        # try to delete deleted user, does not revoke access/refresh tokens
        response = test_client.delete("/user/delete", json=json)
        assert b"user does not exist" in response.data

    def test_register_user(self, test_client, test_users):
        json = set_json_register(0, test_users)
        response = test_client.post("/user", json=json)
        assert b"the user has been created" in response.data
        assert response.status_code == 200

        json = set_json_register(1, test_users)
        response = test_client.post("/user", json=json)
        assert b"Email is already in use" in response.data
        assert response.status_code == 409

        json = set_json_register(2, test_users)
        response = test_client.post("/user", json=json)
        assert b"Username is already in use" in response.data
        assert response.status_code == 409

        json = set_json_register(3, test_users)
        response = test_client.post("/user", json=json)
        assert b"Passwords don't match" in response.data
        assert response.status_code == 400

        json = set_json_register(4, test_users)
        response = test_client.post("/user", json=json)
        assert b"Username is too short" in response.data
        assert response.status_code == 400

        json = set_json_register(5, test_users)
        response = test_client.post("/user", json=json)
        assert b"Password is too short" in response.data
        assert response.status_code == 400

        json = set_json_register(6, test_users)
        response = test_client.post("/user", json=json)
        assert b"Email is invalid" in response.data
        assert response.status_code == 400

    def test_login_user_valid_email_and_password(self, test_client, test_users):
        user = test_users[0]
        json = {"email": test_users[0].email, "password": test_users[0].password1}

        response = test_client.put("/user", json=json)
        data = {
            "access_token": response.json.get("access_token", {}),
            "refresh_token": response.json.get("refresh_token", {}),
        }
        user.login(data["access_token"], data["refresh_token"])
        assert b"successfully logged in" in response.data
        assert response.status_code == 200

    def test_login_user_invalid_email_or_password(self, test_client, test_users):
        # incorrect email
        json = {"email": test_users[2].email, "password": test_users[0].password1}

        response = test_client.put("/user", json=json)
        assert b"Email not found" in response.data
        assert response.status_code == 404

        # incorrect password
        json = {"email": test_users[0].email, "password": test_users[1].password1}

        response = test_client.put("/user", json=json)
        assert b"Password is incorrect" in response.data
        assert response.status_code == 400

    def test_logout_logged_in_user(self, test_client, test_users):
        json = {"access_token": test_users[0].access_token}
        response = test_client.delete("/user", json=json)
        assert b"user logged out" in response.data
        assert response.status_code == 200

    # also tests accessing a page with revoked access token
    # TODO run similar test in test_auth
    def test_logout_logged_out_user(self, test_client, test_users):
        json = {"access_token": test_users[0].access_token}
        response = test_client.delete("/user", json=json)
        assert b"Token has been revoked" in response.data
        assert response.status_code == 401

    # gives stale access_token, need valid refresh_token
    # TODO try to refresh access_token with stale refresh_token
    def test_refresh_access_token(self, test_client, test_users):
        json = {"refresh_token": test_users[0].refresh_token}
        response = test_client.put("/user/refresh", json=json)
        test_users[0].refresh_access_token(response.json.get("access_token", {}))

        assert b"access_token" in response.data
        assert response.status_code == 200

    def test_logout_user_with_stale_access_token(self, test_client, test_users):
        json = {"access_token": test_users[0].access_token}
        response = test_client.delete("/user", json=json)
        assert b"user logged out" in response.data
        assert response.status_code == 200


def set_json_register(user: int, users: list[object]):
    json = {
        "email": users[user].email,
        "username": users[user].username,
        "password1": users[user].password1,
        "password2": users[user].password2,
    }
    return json
