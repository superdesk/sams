from pytest import fixture
from sams_client import Client


@fixture
def client():
    configs = {
        'HOST': 'localhost',
        'PORT': 5700
    }
    return Client(configs)
