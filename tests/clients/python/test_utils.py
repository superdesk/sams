from sams_client.utils import load_configs, get_base_url


configs = {
    'HOST': 'host',
    'PORT': 1234
}

def test_load_configs():
    """Test load_configs in utils
    """
    host, port = load_configs(configs)
    assert host == 'host'
    assert port == 1234

def test_get_base_url():
    """Test get_base_url in utils
    """
    base_url = get_base_url(configs)
    expected_response = 'http://host:1234'
    assert base_url == expected_response
