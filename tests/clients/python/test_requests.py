def test_requests(client):
    """Test request method in SamsClient
    """
    resp = client.request(api='/')
    assert resp.status_code == 200
