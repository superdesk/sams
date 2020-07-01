from sams_client.auth.basic import SamsBasicAuth, get_auth_instance


api_key = 'mock_key'


def test_get_auth_instance():
    auth_instance = get_auth_instance(api_key=api_key)

    assert type(auth_instance) is SamsBasicAuth

    assert auth_instance.api_key == api_key


def test_apply_headers():
    auth_instance = SamsBasicAuth(api_key)
    auth_headers = auth_instance.apply_headers({})

    assert auth_headers['Authorization'] == f'Basic {api_key}'
