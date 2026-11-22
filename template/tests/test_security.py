def test_security_headers(client):
    response = client.get("/healthz")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"


def test_rejects_oversized_payload(app, client):
    app.config["MAX_CONTENT_LENGTH"] = 1024

    response = client.post(
        "/api/echo/string",
        json={"message": "x" * 2048, "echo_type": "None"},
    )

    assert response.status_code == 413, response.text
