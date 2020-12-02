import pytest
from copy import deepcopy
from bson import ObjectId

from superdesk import get_resource_service

from sams.sets import get_service
from sams.storage.destinations import Destination
from sams.storage.providers.mongo import MongoGridFSProvider

from sams_client.schemas.sets import SET_STATES
from sams_client.errors import SamsSetErrors, SamsResourceErrors

from .utils import dict_contains
from tests.fixtures import test_sets, STORAGE_DESTINATIONS


def test_set_is_internal(init_app, client):
    # Make sure this service is for internal consumption only
    resp = client.get('/internal/sets')
    assert resp.status_code == 404

    # Make sure the service exists, otherwise a key exception will be raised here
    service = get_resource_service('sets')
    assert service.find({}).count() == 0


def test_create(init_app, app):
    sets_service = get_service()

    assert sets_service.find({}).count() == 0

    # Test required validation rules
    with pytest.raises(SamsResourceErrors.ValidationError) as error:
        with app.test_request_context():
            sets_service.post([{}])

    assert error.value.errors == dict(
        name=['required'],
        destination_name=['required']
    )

    with app.test_request_context():
        item_id = sets_service.post(deepcopy([test_sets[0]]))[0]

    items = sets_service.find({})
    assert items.count() == 1

    item = items[0]
    assert item['_id'] == item_id
    assert dict_contains(item, test_sets[0])

    item = sets_service.get_by_id(item_id)
    assert item['_id'] == item_id
    assert dict_contains(item, test_sets[0])


def test_update_state(init_app, app):
    sets_service = get_service()

    with app.test_request_context():
        item_id = sets_service.post(deepcopy(test_sets))[0]

        sets_service.patch(item_id, {'state': SET_STATES.DRAFT})
        sets_service.patch(item_id, {'state': SET_STATES.USABLE})
        sets_service.patch(item_id, {'state': SET_STATES.DISABLED})
        sets_service.patch(item_id, {'state': SET_STATES.USABLE})

        with pytest.raises(SamsSetErrors.InvalidStateTransition) as error:
            sets_service.patch(item_id, {'state': SET_STATES.DRAFT})
        assert error.value.description == 'Cannot change state from "{}" to draft'.format(SET_STATES.USABLE)

        sets_service.patch(item_id, {'state': SET_STATES.DISABLED})
        with pytest.raises(SamsSetErrors.InvalidStateTransition) as error:
            sets_service.patch(item_id, {'state': SET_STATES.DRAFT})
        assert error.value.description == 'Cannot change state from "{}" to draft'.format(SET_STATES.DISABLED)


def test_update_destination_name(init_app, app):
    sets_service = get_service()

    with app.test_request_context():
        item_id = sets_service.post(deepcopy(test_sets))[0]

        # can update the destination name while in Draft state
        sets_service.patch(item_id, {'destination_name': 'during_draft'})

        # Change the state to 'usable' then test changing destination name
        sets_service.patch(item_id, {'state': SET_STATES.USABLE})
        with pytest.raises(SamsSetErrors.DestinationChangeNotAllowed):
            sets_service.patch(item_id, {'destination_name': 'after_draft'})

        # Test updating with destination name unchanged
        sets_service.patch(item_id, {'destination_name': 'during_draft'})


def test_validate_destination_name(init_app, app):
    sets_service = get_service()

    def _test_post():
        item = deepcopy(test_sets[0])
        item['destination_name'] = 'unknown'

        with pytest.raises(SamsSetErrors.DestinationNotFound) as error:
            sets_service.post([item])
        assert error.value.description == 'Destination "unknown" isnt configured'

    def _test_patch():
        item_id = sets_service.post(deepcopy(test_sets))[0]

        with pytest.raises(SamsSetErrors.DestinationNotFound) as error:
            sets_service.patch(item_id, {'destination_name': 'unknown'})
        assert error.value.description == 'Destination "unknown" isnt configured'

    with app.test_request_context():
        _test_post()
        _test_patch()


def test_update_destination_config(init_app, app):
    with app.test_request_context():
        sets_service = get_service()

        item_id = sets_service.post(deepcopy(test_sets))[0]

        # can update the destination config while in Draft state
        sets_service.patch(item_id, {'destination_config': {'foo': '456'}})

        # change the state to 'usable' then test changing destination config
        sets_service.patch(item_id, {'state': SET_STATES.USABLE})
        with pytest.raises(SamsSetErrors.DestinationConfigChangeNotAllowed):
            sets_service.patch(item_id, {'destination_config': {'bar': '001'}})

        # test updating with destination config unchanged
        sets_service.patch(item_id, {'destination_config': {'foo': '456'}})


def test_delete(init_app, app):
    with app.test_request_context():
        sets_service = get_service()

        assert sets_service.find({}).count() == 0
        sets_service.post(deepcopy(test_sets))
        sets_service.delete_action({})
        assert sets_service.find({}).count() == 0

        item_id = sets_service.post(deepcopy(test_sets))[0]
        sets_service.patch(item_id, {'state': SET_STATES.USABLE})

        with pytest.raises(SamsSetErrors.CannotDeleteActiveSet):
            sets_service.delete_action({})


def test_get_destination(init_app, app):
    sets_service = get_service()

    test_id = ObjectId()
    with pytest.raises(SamsSetErrors.SetNotFound) as error:
        sets_service.get_destination(test_id)
    assert error.value.description == 'Set with id {} not found'.format(str(test_id))

    with app.test_request_context():
        item_id = sets_service.post(deepcopy(test_sets))[0]
        received = sets_service.get_destination(item_id)
    expected = Destination(STORAGE_DESTINATIONS[0])

    assert received.__dict__ == expected.__dict__


def test_get_provider_instance(init_app, app):
    sets_service = get_service()

    with app.test_request_context():
        item_id = sets_service.post(deepcopy(test_sets))[0]
        provider = sets_service.get_provider_instance(item_id)

    assert isinstance(provider, MongoGridFSProvider)
