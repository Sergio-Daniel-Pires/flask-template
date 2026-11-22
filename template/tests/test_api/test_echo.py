import pytest


class TestEcho:
    @pytest.mark.parametrize("message", ["Hello World", "Echo bot"])
    def test_normal_echo(self, client, message: str):
        req = client.post(
            "/echo/string",
            json={"message": message, "echo_type": "None"},
        )

        assert req.status_code == 200, req.text
        assert req.json["result"] == message
        assert req.json["message"] == "Ok"

    @pytest.mark.parametrize(
        ("echo_type", "expected"),
        [
            ("Reverse", "dlroW olleH"),
            ("Mirror", "Hello World | dlroW olleH"),
        ],
    )
    def test_transformed_echo(self, client, echo_type: str, expected: str):
        req = client.post(
            "/echo/string",
            json={"message": "Hello World", "echo_type": echo_type},
        )

        assert req.status_code == 200, req.text
        assert req.json["result"] == expected

    def test_missing_message_returns_400(self, client):
        req = client.post("/echo/string", json={"echo_type": "None"})

        assert req.status_code == 400, req.text

    def test_invalid_echo_type_returns_400(self, client):
        req = client.post(
            "/echo/string",
            json={"message": "Hello", "echo_type": "Shout"},
        )

        assert req.status_code == 400, req.text
        assert "echo_type" in req.json["errors"]
        assert "Shout" in req.json["errors"]["echo_type"]
