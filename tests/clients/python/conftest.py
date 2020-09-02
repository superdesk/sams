from pytest import fixture
from sams_client import SamsClient


configs = {
    'HOST': 'localhost',
    'PORT': 5700
}


@fixture
def client():
    return SamsClient(configs)
