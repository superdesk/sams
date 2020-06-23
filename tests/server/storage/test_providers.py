import pytest

from sams.storage.providers import Provider, providers
from sams.storage.providers.mongo import MongoGridFSProvider
from sams.errors import SuperdeskApiError

from tests.fixtures import MONGO_STORAGE_PROVIDER


def test_provider_class():
    provider = Provider(MONGO_STORAGE_PROVIDER)

    assert provider.config_string == MONGO_STORAGE_PROVIDER
    assert provider.entries == ['sams.storage.providers.mongo', 'MongoGridFSProvider']
    assert provider.module_name == 'sams.storage.providers.mongo'
    assert provider.class_name == 'MongoGridFSProvider'
    assert provider.klass == MongoGridFSProvider
    assert provider.type_name == MongoGridFSProvider.type_name


def test_register_provider(init_app):
    providers.clear()

    assert providers.all() == {}

    providers.register(MONGO_STORAGE_PROVIDER)

    assert list(providers._providers.keys()) == [MongoGridFSProvider.type_name]
    assert providers._providers[MongoGridFSProvider.type_name].__dict__ == Provider(MONGO_STORAGE_PROVIDER).__dict__

    with pytest.raises(ModuleNotFoundError):
        providers.register('sams.storage.providers.mock.MockFSProvider')


def test_get_provider(init_app):
    assert providers.get(MongoGridFSProvider.type_name).__dict__ == Provider(MONGO_STORAGE_PROVIDER).__dict__

    with pytest.raises(SuperdeskApiError) as error:
        providers.get('mock')

    assert str(error.value) == '404: Provider "mock" not registered with the system'


def test_exists(init_app):
    assert providers.exists(MongoGridFSProvider.type_name)
    assert not providers.exists('mock')
