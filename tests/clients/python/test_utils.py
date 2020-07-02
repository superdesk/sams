from sams_client.utils import load_config

config = {
    'HOST': 'host',
    'PORT': 1234
}


def test_load_config():
    """Test load_config in utils
    """
    configuration = load_config(config)
    assert configuration['base_url'] == 'http://host:1234'
    assert configuration['auth_type'] == 'sams_client.auth.public'
    assert configuration['auth_key'] == ''
