from pytest import fixture
from sams_client import SamsClient
from sams_client.admin_client import SamsClientAdmin


configs = {
    'HOST': 'localhost',
    'PORT': 5000
}


@fixture
def client():
    return SamsClient(configs)


@fixture
def admin_client():
    return SamsClientAdmin(configs)
