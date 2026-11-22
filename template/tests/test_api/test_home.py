def test_home_return_value(client):
    req = client.get("/home/")

    assert req.status_code == 200
    assert req.json["result"] == "Hello World!"
    assert req.json["message"] == "Ok"
