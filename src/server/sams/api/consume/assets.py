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

"""The Assets Consume API allows to search Assets.

This service and resource is intended to be used by external clients.
To access Assets inside the SAMS application, use the :mod:`sams.assets` module instead

Endpoint Attributes
^^^^^^^^^^^^^^^^^^^

=====================   =========================================================
**endpoint name**        'consume_assets'
**resource title**       'Asset'
**resource url**         [GET] '/consume/assets'
**item url**             [GET] '/consume/assets/<:class:`~bson.objectid.ObjectId`>'
**schema**               :attr:`sams_client.schemas.assets.ASSET_SCHEMA`
=====================   =========================================================

HATEOAS
^^^^^^^
The following is a list of extra HATEOAS entries for each Asset returned.

============   ===============   ==========================================================
**Entry**      **Title**         **Href**
============   ===============   ==========================================================
public         Public Asset      Full url to download the file using the SAMS FileServer
============   ===============   ==========================================================

Example Responses
^^^^^^^^^^^^^^^^^

Single Asset::

    curl http://localhost:5700/consume/assets/5f97aea1cb0c490147038936
    {
        "_id": "5f97aea1cb0c490147038936",,
        "_created": "2020-10-27T05:22:41+0000",
        "_updated": "2020-10-27T05:22:41+0000",
        "_etag": "169baf88f70e8233a3e588894bfff379f7dbb0e9",
        "name": "bbb 0004",
        "description": "Big Buck Bunny - Frame 0004",
        "filename": "bbb_0004.png",
        "mimetype": "image/png",
        "length": 18716701,
        "state": "public",
        "set_id": "5f86b3f8cf6caa95368d074e",
        "_links": {
            "self": {
                "title": "Asset",
                "href": "consume/assets/5f97aea1cb0c490147038936"
            },
            "parent": {
                "title": "home",
                "href": "/"
            },
            "collection": {
                "title": "Asset",
                "href": "consume/assets"
            },
            "public": {
                "title": "Public Asset",
                "href": "http://localhost:5750/assets/5f86b3f8cf6caa95368d074e/5f97aea1cb0c490147038936"
            }
        }
    }

Multiple Assets::

    curl http://localhost:5700/consume/assets
    {
        "_items": [{
            "_id": "5f97aea1cb0c490147038936",,
            "_created": "2020-10-27T05:22:41+0000",
            "_updated": "2020-10-27T05:22:41+0000",
            "_etag": "169baf88f70e8233a3e588894bfff379f7dbb0e9",
            "name": "bbb 0004",
            "description": "Big Buck Bunny - Frame 0004",
            "filename": "bbb_0004.png",
            "mimetype": "image/png",
            "length": 18716701,
            "state": "public",
            "set_id": "5f86b3f8cf6caa95368d074e",
            "_links": {
                "self": {
                    "title": "Asset",
                    "href": "consume/assets/5f97aea1cb0c490147038936"
                },
                "public": {
                    "title": "Public Asset",
                    "href": "http://localhost:5750/assets/5f86b3f8cf6caa95368d074e/5f97aea1cb0c490147038936"
                }
            }
        }, {
            "_id": "5f976757663e191130679f8a",
            "_created": "2020-10-27T00:18:31+0000",
            "_updated": "2020-10-27T00:18:31+0000",
            "_etag": "5680e57ddcdf1cf088c8f9ecf3ae0b57850cc288",
            "name": "bbb_0001.png",
            "description": "",
            "filename": "bbb_0001.png",
            "mimetype": "image/png",
            "length": 26413745,
            "state": "draft",
            "set_id": "5f86b3f8cf6caa95368d074e",
            "_links": {
                "self": {
                    "title": "Asset",
                    "href": "consume/assets/5f976757663e191130679f8a"
                }
            }
        }],
        "_links": {
            "parent": {
                "title": "home",
                "href": "/"
            },
            "self": {
                "title": "Asset",
                "href": "consume/assets"
            }
        },
        "_meta": {
            "page": 1,
            "max_results": 25,
            "total": 2
        }
    }

"""

from io import BytesIO
import zipfile
import hashlib

from bson import ObjectId
from flask import request, current_app as app

from superdesk import Blueprint
from superdesk.resource import Resource, build_custom_hateoas

from sams.api.service import SamsApiService
from sams.assets import get_service as get_asset_service
from sams.sets import get_service as get_set_service
from sams.default_settings import strtobool
from sams.utils import construct_asset_download_response

from sams_client.schemas import SET_STATES, ASSET_STATES

assets_bp = Blueprint('assets', __name__)


@assets_bp.route('/consume/assets/binary/<asset_id>', methods=['GET'])
def download_binary(asset_id: str):
    """
    Uses asset_id and returns the corresponding
    asset binary
    """

    service = get_asset_service()
    asset = service.get_by_id(asset_id)
    file = service.download_binary(asset_id)

    return construct_asset_download_response(asset, file)


@assets_bp.route('/consume/assets/compressed_binary/<asset_ids>', methods=['GET'])
def download_compressed_binary(asset_ids: str):
    """
    Uses asset_ids and returns the compressed
    asset binaries zip
    """
    service = get_asset_service()
    split_asset_ids = asset_ids.split(',')

    file = [service.download_binary(ObjectId(asset_id)) for asset_id in split_asset_ids]
    files = [(single_file.filename, single_file.read()) for single_file in file]

    in_memory_zip = BytesIO()
    with zipfile.ZipFile(in_memory_zip, mode='w') as temp_zip:
        for f in files:
            temp_zip.writestr(f[0], f[1])
    data = in_memory_zip.getvalue()
    response = app.response_class(
        data,
        content_type='application/zip',
        direct_passthrough=True
    )

    response.content_length = len(data)
    h = hashlib.sha1()
    h.update(data)
    response.set_etag(h.hexdigest())

    if strtobool(request.args.get('download', 'False')):
        response.headers['Content-Disposition'] = 'Attachment'
    else:
        response.headers['Content-Disposition'] = 'Inline'
    return response


class ConsumeAssetResource(Resource):
    endpoint_name = 'consume_assets'
    resource_title = 'Asset'
    url = 'consume/assets'
    item_methods = ['GET']
    resource_methods = ['GET']
    allow_unknown = True


class ConsumeAssetService(SamsApiService):
    def on_fetched_item(self, doc):
        if app.config.get('SAMS_PUBLIC_URL'):
            self.enhance_items_with_public_url([doc])
        else:
            self.enhance_items([doc])

    def on_fetched(self, doc):
        if app.config.get('SAMS_PUBLIC_URL'):
            self.enhance_items_with_public_url(doc['_items'])
        else:
            self.enhance_items(doc['_items'])

    def enhance_items(self, docs):
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

    def enhance_items_with_public_url(self, docs):
        public_set_query = {
            '_id': {
                '$in': [
                    asset['set_id']
                    for asset in docs
                ]
            },
            'state': SET_STATES.USABLE
        }
        public_set_ids = [
            str(item['_id'])
            for item in get_set_service().get(req=None, lookup=public_set_query)
        ]
        public_url = app.config['SAMS_PUBLIC_URL'].rstrip('/')

        for doc in docs:
            hateoas = {
                'self': {
                    'title': ConsumeAssetResource.resource_title,
                    'href': ConsumeAssetResource.url + '/{_id}'
                },
            }

            if str(doc['set_id']) in public_set_ids and doc['state'] == ASSET_STATES.PUBLIC:
                hateoas['public'] = {
                    'title': 'Public Asset',
                    'href': public_url + '/assets/{set_id}/{_id}'
                }

            build_custom_hateoas(
                hateoas,
                doc,
                _id=str(doc.get('_id')),
                set_id=str(doc.get('set_id')),
            )
