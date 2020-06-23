import pytest

from sams.errors import SuperdeskApiError
from sams.storage.destinations import Destination, destinations
from sams.storage.providers import providers, Provider

from tests.fixtures import STORAGE_DESTINATIONS, MONGO_STORAGE_PROVIDER


def test_destination_class():
    providers.register(MONGO_STORAGE_PROVIDER)
    destination = Destination(STORAGE_DESTINATIONS[0])

    assert destination.config_string == STORAGE_DESTINATIONS[0]
    assert destination.entries == ['MongoGridFS', 'internal', 'mongodb://localhost/tests_sams']
    assert destination.name == 'internal'
    assert destination.provider_name == 'MongoGridFS'
    assert destination.config == 'mongodb://localhost/tests_sams'
    assert destination.provider.__dict__ == Provider(MONGO_STORAGE_PROVIDER).__dict__


def test_register_destination(init_app):
    destinations.clear()

    assert destinations._destinations == {}

    destinations.register(STORAGE_DESTINATIONS[0])

    assert list(destinations._destinations.keys()) == ['internal']
    assert destinations._destinations['internal'].__dict__ == Destination(STORAGE_DESTINATIONS[0]).__dict__

    with pytest.raises(SuperdeskApiError) as error:
        destinations.register('MockProvider,mock,mongodb://localhost/tests_sams')

    assert str(error.value) == '404: Provider "MockProvider" not registered with the system'


def test_get_destination(init_app):
    assert destinations.get('internal').__dict__ == Destination(STORAGE_DESTINATIONS[0]).__dict__

    with pytest.raises(SuperdeskApiError) as error:
        destinations.get('mock')

    assert str(error.value) == '404: Destination "mock" not registered with the system'


def test_exists(init_app):
    assert destinations.exists('internal')
    assert not destinations.exists('mock')
