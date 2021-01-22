#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# This file is part of SAMS.
#
# Copyright 2020 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""The Assets Admin API allows to create, update or delete Assets.

This service and resource is intended to be used by external clients.
To access Assets inside the SAMS application, use the :mod:`sams.assets` module instead

=====================   =================================================================
**endpoint name**        'produce/assets'
**resource title**       'Asset'
**resource url**         [POST] '/produce/assets'
**item url**             [PATCH, DELETE] '/produce/assets/<:class:`~bson.objectid.ObjectId`>'
**schema**               :attr:`sams_client.schemas.assets.ASSET_SCHEMA`
=====================   =================================================================
"""
from bson import ObjectId
from flask import current_app as app, json
from flask import request

from sams.api.service import SamsApiService
from sams.api.consume import ConsumeAssetResource
from sams_client.schemas import SET_STATES
from sams.sets import get_service as get_sets_service
from sams.assets import get_service as get_asset_service
from sams.storage.sams_media_storage import get_request_id
from superdesk.resource import Resource, build_custom_hateoas
from sams_client.errors import SamsAssetErrors
from sams.utils import get_external_user_id, get_external_session_id

from superdesk import Blueprint
from superdesk.utc import utcnow

FIELDS_TO_JSON_PARSE = ('tags', 'extra')

assets_produce_bp = Blueprint('assets_produce', __name__)


@assets_produce_bp.route('/produce/assets/lock/<asset_id>', methods=['PATCH'])
def lock_asset(asset_id: str):
    """
    Uses asset_id and lock action and locks the corresponding asset
    """

    service = get_asset_service()
    asset = service.get_by_id(asset_id)
    lock_action = request.json.get('lock_action', None)
    updates = {}

    if asset.get('lock_action', None) is not None:
        raise SamsAssetErrors.LockingAssetLocked()

    external_user_id = get_external_user_id()
    external_session_id = get_external_session_id()

    if not external_user_id:
        raise SamsAssetErrors.ExternalUserIdNotFound()

    if not external_session_id:
        raise SamsAssetErrors.ExternalSessionIdNotFound()

    updates['lock_action'] = lock_action
    updates['lock_user'] = external_user_id
    updates['lock_session'] = external_session_id
    updates['lock_time'] = utcnow()

    return service.patch(ObjectId(asset_id), updates)


@assets_produce_bp.route('/produce/assets/unlock/<asset_id>', methods=['PATCH'])
def unlock_asset(asset_id: str):
    """
    Uses asset_id and unlocks the corresponding asset
    """

    service = get_asset_service()
    asset = service.get_by_id(asset_id)
    updates = {}

    force = request.json.get('force', None)
    if force:
        updates['lock_action'] = None
        updates['lock_user'] = None
        updates['lock_session'] = None
        updates['lock_time'] = None

    else:
        if asset.get('lock_action', None) is None:
            raise SamsAssetErrors.UnlockingAssetUnlocked()

        external_user_id = get_external_user_id()
        external_session_id = get_external_session_id()

        if not external_user_id:
            raise SamsAssetErrors.ExternalUserIdNotFound()

        if not external_session_id:
            raise SamsAssetErrors.ExternalSessionIdNotFound()

        if asset['lock_user'] != external_user_id:
            raise SamsAssetErrors.ExternalUserIdDoNotMatch()

        if asset['lock_session'] != external_session_id:
            raise SamsAssetErrors.ExternalSessionIdDoNotMatch()

        updates['lock_action'] = None
        updates['lock_user'] = None
        updates['lock_session'] = None
        updates['lock_time'] = None

    return service.patch(ObjectId(asset_id), updates)


@assets_produce_bp.route('/produce/assets/unlock_user_session', methods=['PATCH'])
def unlock_asset_by_user():
    """
    Uses user_id, session_id and unlocks the corresponding assets
    """

    external_user_id = get_external_user_id()
    external_session_id = get_external_session_id()
    service = get_asset_service()

    assets = service.search({
        'query': {
            'bool': {
                'must': [
                    {'term': {'lock_user': external_user_id}},
                    {'term': {'lock_session': external_session_id}}
                ]
            }
        }
    })

    for asset in assets:
        updates = {}
        updates['lock_action'] = None
        updates['lock_user'] = None
        updates['lock_session'] = None
        updates['lock_time'] = None

        service.patch(ObjectId(asset['_id']), updates)

    response = app.response_class(
        status=200,
    )
    return response


class ProduceAssetResource(Resource):
    endpoint_name = 'produce_assets'
    resource_title = 'Asset'
    url = 'produce/assets'
    item_methods = ['PATCH', 'DELETE']
    resource_methods = ['POST']
    schema = {
        'binary': {
            'type': 'media',
            'required': False
        }
    }
    allow_unknown = True


class ProduceAssetService(SamsApiService):
    def on_created(self, docs):
        for doc in docs:
            build_custom_hateoas(
                {
                    'self': {
                        'title': ConsumeAssetResource.resource_title,
                        'href': ConsumeAssetResource.url + '/{_id}'
                    }
                },
                doc,
                _id=str(doc.get('_id'))
            )

    def on_create(self, docs):
        for doc in docs:
            for field in FIELDS_TO_JSON_PARSE:
                if isinstance(doc.get(field), str):
                    doc[field] = json.loads(doc[field])

    def create(self, docs, **lookup):
        """
        Creates new asset
        """
        # Get set state using internal sets service
        sets_service = get_sets_service()
        state = sets_service.get_by_id(docs[0]['set_id']).get('state')

        # Raise error if set state is 'draft' or 'disabled'
        if state in [SET_STATES.DRAFT, SET_STATES.DISABLED]:
            raise SamsAssetErrors.AssetUploadToInactiveSet()

        request_id = get_request_id()
        # Get the binary from storage media cache
        try:
            binary = app.media.cache[request_id]
        except KeyError:
            raise SamsAssetErrors.BinaryNotSupplied()

        # Clear the cache
        app.media.cache.pop(request_id)
        docs[0]['binary'] = binary
        return super().create(docs)

    def update(self, id, updates, original):
        """
        Uses 'id' and updates the corresponding asset
        """
        # Get set state using internal sets service
        sets_service = get_sets_service()
        state = sets_service.get_by_id(original.get('set_id')).get('state')

        # Raise error if set state is 'draft' or 'disabled'
        if state in [SET_STATES.DRAFT, SET_STATES.DISABLED]:
            raise SamsAssetErrors.AssetUploadToInactiveSet()

        request_id = get_request_id()
        # If binary is not to be updated pass
        try:
            binary = app.media.cache[request_id]
            app.media.cache.pop(request_id)
            updates['binary'] = binary
        except KeyError:
            pass
        return super().update(id, updates, original)
