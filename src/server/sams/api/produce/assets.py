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
from sams.api.service import SamsApiService
from sams.api.consume import ConsumeAssetResource
from sams_client.schemas import ASSET_SCHEMA
from sams_client.schemas import SET_STATES
from sams.sets import get_service
from sams.storage.sams_media_storage import get_request_id
from superdesk.errors import SuperdeskApiError
from superdesk.resource import Resource, build_custom_hateoas


class ProduceAssetResource(Resource):
    endpoint_name = 'produce_assets'
    resource_title = 'Asset'
    url = 'produce/assets'
    item_methods = ['PATCH', 'DELETE']
    resource_methods = ['POST']
    schema = ASSET_SCHEMA


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

    def create(self, docs, **lookup):
        """
        Creates new asset
        """
        sets_service = get_service()
        state = sets_service.get_by_id(docs[0]['set_id']).get('state')
        # Raise error if set state is 'draft' or 'disabled'
        if state in [SET_STATES.DRAFT, SET_STATES.DISABLED]:
            raise SuperdeskApiError.badRequestError(
                'Asset upload is not allowed, set is in {} state'.format(state)
            )
        request_id = get_request_id()
        # Get the binary from storage media cache
        binary = self.app.media.cache[request_id]
        # Clear the cache
        self.app.media.cache.pop(request_id)
        docs[0]['binary'] = binary
        return super().create(docs)

    def update(self, id, updates, original):
        """
        Uses 'id' and updates the corresponding asset
        """
        request_id = get_request_id()
        # If binary is not to be updated pass
        try:
            binary = self.app.media.cache[request_id]
            self.app.media.cache.pop(request_id)
            updates['binary'] = binary
        except KeyError:
            pass
        return super().update(id, updates, original)
