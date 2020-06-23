def test_requests(client):
    resp = client.request(api='/')
    assert resp.status_code == 200
