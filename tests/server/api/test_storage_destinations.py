import pytest
from sams.api.admin import get_service
from sams.errors import SuperdeskApiError
from sams.storage.destinations import Destination, destinations
from tests.fixtures import STORAGE_DESTINATIONS


def test_get(init_app):
    destination_service = get_service()

    response = destination_service.get(req=None)

    assert response.count() == len(STORAGE_DESTINATIONS)
    assert list(map(
        lambda destination: destination.to_dict(),
        destinations._destinations.values()
    )) == response.docs


def test_find_one(init_app):
    destination_service = get_service()

    with pytest.raises(SuperdeskApiError) as error:
        destination_service.find_one(req=None, _id='mock')

    assert str(error.value) == '404: Destination "mock" not registered with the system'

    assert destination_service.find_one(req=None, _id='internal') == Destination(STORAGE_DESTINATIONS[0]).to_dict()
