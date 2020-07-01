from sams_client.auth.public import SamsPublicAuth, get_auth_instance


def test_get_auth_instance():
    auth_instance = get_auth_instance()

    assert type(auth_instance) is SamsPublicAuth


def test_apply_headers():
    auth_instance = SamsPublicAuth()

    expected = [
        {}, {'mock_key': 'mock_value'}
    ]

    recieved = list(map(
        auth_instance.apply_headers,
        expected
    ))

    assert expected == recieved
