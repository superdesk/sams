from sams_client.utils import load_configs


def test_load_configs():
    configs = {
        'HOST': 'host',
        'PORT': 1234
    }
    host, port = load_configs(configs)
    assert host == 'host'
    assert port == 1234
