from test_user_handlers import set_json_register

# TODO accessing required fresh page with fresh access_token


class TestAuth:
    def test_access_url_with_revoked_access_token(self, test_client, test_users):
        # register user
        json = set_json_register(0, test_users)
        response = test_client.post("/user", json=json)

        # login user
        json = {"email": test_users[0].email, "password": test_users[0].password1}
        response = test_client.put("/user", json=json)

        # logout user
        json = {"access_token": response.json.get("access_token", {})}
        response = test_client.delete("/user", json=json)

        # try to logout again with invalidated token
        response = test_client.delete("/user", json=json)
        assert b"Token has been revoked" in response.data
        assert response.status_code == 401

    def test_access_url_with_invalid_access_token(self, test_client, test_users):
        # not enough segments
        bad_access_token = {"access_token": "4"}
        response = test_client.get("/stocks", json=bad_access_token)
        assert b"Not enough segments" in response.data

        # invalid header padding
        bad_access_token = {"access_token": "4.4.4"}
        response = test_client.get("/stocks", json=bad_access_token)
        assert b"Invalid header padding" in response.data

        # invalid payload padding
        bad_access_token = {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.4.4"}
        response = test_client.get("/stocks", json=bad_access_token)
        assert b"Invalid payload padding" in response.data

        # invalid crypto padding
        bad_access_token = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQzNTY3MzczLCJqdGkiOiJhNj.4"
        }
        response = test_client.get("/stocks", json=bad_access_token)
        assert b"Invalid crypto padding" in response.data

        # invalid payload string
        bad_access_token = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQzNTY3MzczLCJqdGkiOiJhNj.s4sv-QqJhVq4cfu2cmhtB5X6P-i8ZyqEbUoKT94GswU"
        }
        response = test_client.get("/stocks", json=bad_access_token)
        assert b"Invalid payload string" in response.data

        # signature verification failed
        bad_access_token = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQzNTY3NTk1LCJqdGkiOiIzMDExZTQzOC0zN2YyLTRmMTEtOGQ0Yy1mYjYxNGE4ZjJmYTUiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidXNlcm5hbWUzMCIsIm5iZiI6MTY0MzU2NzU5NSwiZXhwIjoxNjQzNTY5Mzk1fQ.lB0eR_azUVlrvYH92cWBT3CKJWKejzrIVP2y31_9MTk"
        }
        response = test_client.get("/stocks", json=bad_access_token)
        assert b"Signature verification failed" in response.data

    def test_accessing_url_without_access_token_for_jwt_required_url(self, test_client):
        # missing access_token key
        json = {}
        response = test_client.get("/stocks", json=json)
        assert b"Missing" in response.data

    def test_accessing_url_with_stale_access_token_for_jwt_not_required_url(
        self, test_client, test_users
    ):
        # login user
        json = {"email": test_users[0].email, "password": test_users[0].password1}
        response = test_client.put("/user", json=json)

        # get stale token
        json = {"refresh_token": response.json.get("refresh_token", {})}
        response = test_client.put("/user/refresh", json=json)

        # access url with stale token
        json = {"access_token": response.json.get("access_token", {})}
        response = test_client.get("/stocks", json=json)

        assert b"[]" in response.data
        assert response.status_code == 200

    def test_accessing_url_with_fresh_access_token_for_jwt_not_required_url(
        self, test_client, test_users
    ):
        # login user
        json = {"email": test_users[0].email, "password": test_users[0].password1}
        response = test_client.put("/user", json=json)

        # access url with fresh token
        json = {"access_token": response.json.get("access_token", {})}
        response = test_client.get("/stocks", json=json)

        assert b"[]" in response.data
        assert response.status_code == 200

    def test_access_required_fresh_url_with_stale_access_token(
        self, test_client, test_users
    ):
        # login user
        json = {"email": test_users[0].email, "password": test_users[0].password1}
        response = test_client.put("/user", json=json)

        # get stale token
        json = {"refresh_token": response.json.get("refresh_token", {})}
        response = test_client.put("/user/refresh", json=json)

        # access url with stale token
        json = {"access_token": response.json.get("access_token", {})}
        response = test_client.delete("/user/delete", json=json)

        assert b"Fresh token required" in response.data
        assert response.status_code == 401

    def test_access_required_fresh_url_with_fresh_access_token(
        self, test_client, test_users
    ):
        # login user
        json = {"email": test_users[0].email, "password": test_users[0].password1}
        response = test_client.put("/user", json=json)

        # access url with fresh token
        json = {"access_token": response.json.get("access_token", {})}
        response = test_client.delete("/user/delete", json=json)

        assert b"user deleted successfully" in response.data
        assert response.status_code == 200
