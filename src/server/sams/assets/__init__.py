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

"""Asset service, used for CRUD operations on Asset metadata and associated binary data.

Usage
-----
The Asset service instance can be found under :data:`sams.assets.get_service` and used::

    from sams.assets import get_service

    def test_assets():
        assets_service = get_service()

        assets_service.post([{...}])
        assets_service.patch(asset_id, {...})
        assets_service.delete_action({...})
        assets_service.find({...})

This service instance can only be used after the application has bootstrapped

Example usage of uploading Asset Metadata and Binary::

    from bson import ObjectId
    from sams.assets import get_service

    def test_upload_file(set_id: ObjectId):
        asset_service = get_service()

        with open('tests/fixtures/file_example-jpg.jpg', 'rb') as f:
            asset_service.post([{
                'set_id': set_id,
                'filename': 'file_example-jpg.jpg',
                'name': 'Jpeg Example',
                'description': 'Jpeg file asset example',
                'binary': f
            }])

        # With the above, the system will automatically set:
        {
            '_media_id': '5f16394239d0077e02b09d85',
            'length': 12186,
            'mimetype': 'image/jpeg'
        }
"""

from superdesk import get_backend
from sams.factory.app import SamsApp
from .resource import AssetsResource
from .service import AssetsService

_service: AssetsService


def get_service() -> AssetsService:
    return _service


def init_app(app: SamsApp):
    global _service

    _service = AssetsService(
        AssetsResource.endpoint_name,
        backend=get_backend()
    )
    AssetsResource(
        endpoint_name=AssetsResource.endpoint_name,
        app=app,
        service=_service
    )
