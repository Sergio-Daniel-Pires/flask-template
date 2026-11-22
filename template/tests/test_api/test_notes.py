def test_create_and_list_notes(client):
    created = client.post("/api/notes/", json={"text": "  Primeira nota  "})

    assert created.status_code == 201, created.text
    assert created.json["result"]["text"] == "Primeira nota"
    assert created.json["result"]["created_at"]

    listing = client.get("/api/notes/")

    assert listing.status_code == 200, listing.text
    assert [note["text"] for note in listing.json["result"]] == ["Primeira nota"]


def test_rejects_blank_note(client):
    response = client.post("/api/notes/", json={"text": "   "})

    assert response.status_code == 400, response.text
    assert "must not be empty" in response.json["message"]


def test_rejects_too_long_note(client):
    response = client.post("/api/notes/", json={"text": "x" * 501})

    assert response.status_code == 400, response.text
    assert "too long" in response.json["errors"]["text"]
