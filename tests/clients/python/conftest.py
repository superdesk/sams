from pytest import fixture
from sams_client import SamsClient


@fixture
def client():
    configs = {
        'HOST': 'localhost',
        'PORT': 5000
    }
    return SamsClient(configs)
