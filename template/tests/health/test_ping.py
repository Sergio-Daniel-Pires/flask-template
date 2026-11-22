import pytest


class TestRoutes:
    @pytest.mark.parametrize(
        "route_url",
        ["/", "/healthz", "/api/docs", "/api/home/"],
    )
    def test_known_routes(self, client, route_url: str):
        req = client.get(route_url)

        assert req.status_code == 200, req.text

    @pytest.mark.parametrize("route_url", ["/home/", "/api/missing/"])
    def test_unknown_routes(self, client, route_url: str):
        req = client.get(route_url)

        assert req.status_code == 404, req.text

    def test_health_payload(self, client):
        req = client.get("/healthz")

        assert req.json["status"] == "ok"
        assert req.json["version"]
