import time


class TestAuth:
    def test_access_url_with_revoked_access_token(
        self, test_client: object, test_users: list[object]
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        user.logout(test_client)

        response = test_client.delete("/user", json=user.tokens())

        assert b"Token has been revoked" in response.data
        assert response.status_code == 401

    def test_access_url_with_invalid_access_token_not_enough_segments(
        self, test_client: object
    ) -> None:
        bad_access_token = {"access_token": "4"}
        response = test_client.get("/stocks", json=bad_access_token)

        assert b"Not enough segments" in response.data

    def test_access_url_with_invalid_access_token_invalid_header_padding(
        self, test_client: object
    ) -> None:
        bad_access_token = {"access_token": "4.4.4"}
        response = test_client.get("/stocks", json=bad_access_token)

        assert b"Invalid header padding" in response.data

    def test_access_url_with_invalid_access_token_invalid_payload_padding(
        self, test_client: object
    ) -> None:
        bad_access_token = {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.4.4"}
        response = test_client.get("/stocks", json=bad_access_token)

        assert b"Invalid payload padding" in response.data

    def test_access_url_with_invalid_access_token_invalid_crypto_padding(
        self, test_client: object
    ) -> None:
        bad_access_token = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQzNTY3MzczLCJqdGkiOiJhNj.4"
        }
        response = test_client.get("/stocks", json=bad_access_token)

        assert b"Invalid crypto padding" in response.data

    def test_access_url_with_invalid_access_token_invalid_payload_string(
        self, test_client: object
    ) -> None:
        bad_access_token = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQzNTY3MzczLCJqdGkiOiJhNj.s4sv-QqJhVq4cfu2cmhtB5X6P-i8ZyqEbUoKT94GswU"
        }
        response = test_client.get("/stocks", json=bad_access_token)

        assert b"Invalid payload string" in response.data

    def test_access_url_with_invalid_access_token_signature_verification_failed(
        self, test_client: object
    ) -> None:
        bad_access_token = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQzNTY3NTk1LCJqdGkiOiIzMDExZTQzOC0zN2YyLTRmMTEtOGQ0Yy1mYjYxNGE4ZjJmYTUiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidXNlcm5hbWUzMCIsIm5iZiI6MTY0MzU2NzU5NSwiZXhwIjoxNjQzNTY5Mzk1fQ.lB0eR_azUVlrvYH92cWBT3CKJWKejzrIVP2y31_9MTk"
        }
        response = test_client.get("/stocks", json=bad_access_token)

        assert b"Signature verification failed" in response.data

    def test_accessing_url_without_access_token_for_jwt_required_url(
        self, test_client: object
    ) -> None:
        json = {}
        response = test_client.get("/stocks", json=json)

        assert b"Missing" in response.data

    def test_accessing_url_with_stale_access_token_for_jwt_not_required_url(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.login(test_client)
        user.refresh_access_token(test_client)

        response = test_client.get("/stocks", json=user.tokens())

        assert b"[]" in response.data
        assert response.status_code == 200

    def test_accessing_url_with_fresh_access_token_for_jwt_not_required_url(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.login(test_client)

        response = test_client.get("/stocks", json=user.tokens())

        assert b"[]" in response.data
        assert response.status_code == 200

    def test_access_required_fresh_url_with_stale_access_token(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.login(test_client)
        user.refresh_access_token(test_client)

        response = test_client.delete("/user/delete", json=user.tokens())

        assert b"Fresh token required" in response.data
        assert response.status_code == 401

    def test_access_required_fresh_url_with_fresh_access_token(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.login(test_client)

        response = test_client.delete("/user/delete", json=user.tokens())

        assert b"user deleted successfully" in response.data
        assert response.status_code == 200

    def test_using_expired_refresh_token(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        time.sleep(6)

        response = test_client.put("/user/refresh", json=user.tokens())

        assert b"invalid token or token expired" in response.data
        assert response.status_code == 401

    def test_using_expired_access_token(
        self, test_client: object, test_users: list
    ) -> None:
        user = test_users[0]
        user.register(test_client)
        user.login(test_client)
        time.sleep(6)

        response = test_client.delete("/user/delete", json=user.tokens())

        assert b"invalid token or token expired" in response.data
        assert response.status_code == 401
