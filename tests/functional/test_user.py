class TestUser:
    def test_register_user(self, test_client, new_user):
        json = {
            "email": new_user.email,
            "username": new_user.username,
            "password1": new_user.password1,
            "password2": new_user.password2,
        }
        response = test_client.post("/user", json=json)
        print(response.json)
        assert b"Email is already in use." in response.data
