from sams_client.admin import SamsClientAdmin


def test_request_destinations(admin_client):
    response = admin_client.request_destinations()
    assert response.status_code == 200
    assert response.json()['_items'] == []


def test_request_destination(admin_client):
    destination_name = 'mock'
    response = admin_client.request_destination(id=destination_name)
    assert response.status_code == 404
