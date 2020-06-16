import pytest

from superdesk import get_resource_service
from superdesk.validation import ValidationError

from sams.sets import service as sets_service
from sams.sets.resource import SET_STATES

from .utils import dict_contains

test_sets = [{
    'name': 'Test_Set',
    'state': 'draft',
    'description': 'Set used for testing purposes',
    'destination_name': 'internal',
    'destination_config': {'test': '123'}
}]


def test_set_is_internal(init_app, client):
    # Make sure this service is for internal consumption only
    resp = client.get('/internal/sets')
    assert resp.status_code == 404

    # Make sure the service exists, otherwise a key exception will be raised here
    service = get_resource_service('sets')
    assert service.find({}).count() == 0


def test_create(init_app):
    assert sets_service.find({}).count() == 0

    # Test required validation rules
    with pytest.raises(ValidationError) as error:
        sets_service.post([{}])

    assert list(error.value.args) == [{
        'name': {'required': 1},
        'destination_name': {'required': 1}
    }]

    item_id = sets_service.post(test_sets)[0]

    items = sets_service.find({})
    assert items.count() == 1

    item = items[0]
    assert item['_id'] == item_id
    assert dict_contains(item, test_sets[0])

    item = sets_service.get_by_id(item_id)
    assert item['_id'] == item_id
    assert dict_contains(item, test_sets[0])


def test_update_state(init_app):
    item_id = sets_service.post(test_sets)[0]

    sets_service.patch(item_id, {'state': SET_STATES.DRAFT})
    sets_service.patch(item_id, {'state': SET_STATES.USABLE})
    sets_service.patch(item_id, {'state': SET_STATES.DISABLED})
    sets_service.patch(item_id, {'state': SET_STATES.USABLE})

    with pytest.raises(ValidationError) as error:
        sets_service.patch(item_id, {'state': SET_STATES.DRAFT})
    assert list(error.value.args) == [{
        'state': 'Cannot change state from "{}" to draft'.format(SET_STATES.USABLE)
    }]

    sets_service.patch(item_id, {'state': SET_STATES.DISABLED})
    with pytest.raises(ValidationError) as error:
        sets_service.patch(item_id, {'state': SET_STATES.DRAFT})
    assert list(error.value.args) == [{
        'state': 'Cannot change state from "{}" to draft'.format(SET_STATES.DISABLED)
    }]


def test_update_destination_name(init_app):
    item_id = sets_service.post(test_sets)[0]

    # can update the destination name while in Draft state
    sets_service.patch(item_id, {'destination_name': 'during_draft'})

    # Change the state to 'usable' then test changing destination name
    sets_service.patch(item_id, {'state': SET_STATES.USABLE})
    with pytest.raises(ValidationError) as error:
        sets_service.patch(item_id, {'destination_name': 'after_draft'})

    assert list(error.value.args) == [{
        'destination_name': 'Destination can only be changed in draft state'
    }]

    # Test updating with destination name unchanged
    sets_service.patch(item_id, {'destination_name': 'during_draft'})


def test_update_destination_config(init_app):
    item_id = sets_service.post(test_sets)[0]

    # can update the destination config while in Draft state
    sets_service.patch(item_id, {'destination_config': {'foo': '456'}})

    # change the state to 'usable' then test changing destination config
    sets_service.patch(item_id, {'state': SET_STATES.USABLE})
    with pytest.raises(ValidationError) as error:
        sets_service.patch(item_id, {'destination_config': {'bar': '001'}})

    assert list(error.value.args) == [{
        'destination_config': 'Destination config can only be changed in draft state'
    }]

    # test updating with destination config unchanged
    sets_service.patch(item_id, {'destination_config': {'foo': '456'}})


def test_delete(init_app):
    assert sets_service.find({}).count() == 0
    sets_service.post(test_sets)
    sets_service.delete_action({})
    assert sets_service.find({}).count() == 0

    item_id = sets_service.post(test_sets)[0]
    sets_service.patch(item_id, {'state': SET_STATES.USABLE})

    with pytest.raises(ValidationError) as error:
        sets_service.delete_action({})

    assert list(error.value.args) == [{
        'delete': 'Can only delete Sets that are in draft state'
    }]
