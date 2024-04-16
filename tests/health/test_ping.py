import pytest


class TestGetRoutes:
    @pytest.mark.parametrize("route_url", [ "/home/" ])
    def test_known_routes (self, client, route_url: str):
        with client:
            req = client.get(route_url)

            assert req.status_code == 200

    @pytest.mark.parametrize("route_url", [ "/home2/" ])
    def test_unknown_routes (self, client, route_url: str):
        with client:
            req = client.get(route_url)

            assert req.status_code == 404
