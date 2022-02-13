class TestExtraRoutes:
    def test_main_url(self, test_client: object) -> None:
        response = test_client.get("/")
        assert b"github" in response.data
        assert response.status_code == 200
