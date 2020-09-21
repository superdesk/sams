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

=====================   =========================================================
**endpoint name**        'consume_assets'
**resource title**       'Asset'
**resource url**         [GET] '/consume/assets'
**item url**             [GET] '/consume/assets/<:class:`~bson.objectid.ObjectId`>'
**schema**               :attr:`sams_client.schemas.assets.ASSET_SCHEMA`
=====================   =========================================================
"""

import superdesk
import zipfile
from bson import ObjectId
from io import BytesIO
from flask import request, current_app as app
from sams.api.service import SamsApiService
from sams.assets import get_service as get_asset_service
from sams.default_settings import strtobool
from superdesk.resource import Resource, build_custom_hateoas
from werkzeug.wsgi import wrap_file
from sams.default_settings import strtobool

assets_bp = superdesk.Blueprint('assets', __name__)
cache_for = 3600 * 24 * 30  # 30d cache


@assets_bp.route('/consume/assets/binary/<asset_id>', methods=['GET'])
def download_binary(asset_id):
    """
    Uses asset_id and returns the corresponding
    asset binary
    """

    service = get_asset_service()
    asset = service.get_by_id(asset_id)
    file = service.download_binary(asset_id)
    data = wrap_file(request.environ, file, buffer_size=1024 * 256)
    response = app.response_class(
        data,
        mimetype=asset['mimetype'],
        direct_passthrough=True
    )
    response.content_length = asset['length']
    response.last_modified = asset['_updated']
    response.set_etag(asset['_etag'])
    response.cache_control.max_age = cache_for
    response.cache_control.s_max_age = cache_for
    response.cache_control.public = True
    response.make_conditional(request)

    if strtobool(request.args.get('download', 'False')):
        response.headers['Content-Disposition'] = 'Attachment; filename={}'.format(asset['filename'])
    else:
        response.headers['Content-Disposition'] = 'Inline; filename={}'.format(asset['filename'])

    return response


@assets_bp.route('/consume/assets/compressed_binary/<asset_ids>', methods=['GET'])
def download_compressed_binary(asset_ids):
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
        self.enhance_items([doc])

    def on_fetched(self, doc):
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
