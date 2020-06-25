from sams_client.admin import SamsClientAdmin


def test_request_destination(admin_client):
    response = admin_client.request_destinations()
    expected_response = []
    assert response == expected_response
