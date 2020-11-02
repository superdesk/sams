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

"""An Asset Binary API intended for public consumption.

This service provides a single endpoint, to download the binary of an Asset.
No metadata will be available to the client, nor will any specific errors be returned.

=====================   =========================================================
**endpoint name**        'public_assets'
**resource title**       'Asset'
**item url**             [GET] '/assets/``<set_id>``/``<asset_id>``'
=====================   =========================================================


The following validation occurs on this endpoint:

    * ``set_id`` must be a valid :class:`bson.objectid.ObjectId`
    * ``asset_id`` must be a valid :class:`bson.objectid.ObjectId`
    * The ``Set`` with ``_id == set_id`` must exist
    * The ``Set`` must have ``state == 'usable'``
    * The ``Asset`` with ``_id == asset_id`` must exist
    * The ``Asset`` must be stored in the ``Set``
    * The ``Asset`` must have ``state == 'public'``

If any of the above conditions are not met, a ``404 - Not Found`` error is returned.
"""

from typing import Union, Tuple

from bson import ObjectId
from flask import Response

from superdesk import Blueprint

from sams.sets import get_service as get_set_service
from sams.assets import get_service as get_asset_service
from sams.logger import logger
from sams.utils import construct_asset_download_response

from sams_client.schemas import SET_STATES, ASSET_STATES


asset_binary_bp = Blueprint('assets_binary', __name__)


@asset_binary_bp.route('/assets/<set_id>/<asset_id>', methods=['GET'])
def download_binary(set_id: str, asset_id: str) -> Union[Response, Tuple[str, int]]:
    # Make sure the provided ids are valid ObjectIds. If not then fail early
    try:
        set_oid = ObjectId(set_id)
        asset_oid = ObjectId(asset_id)
    except Exception:
        return '', 404

    set_service = get_set_service()
    asset_service = get_asset_service()

    try:
        set_item = set_service.get_by_id(set_oid)
    except Exception as e:
        logger.exception(e)
        return '', 404

    # Make sure the Set exists and has a state of `usable`
    if not set_item or set_item.get('state') != SET_STATES.USABLE:
        return '', 404

    try:
        metadata = asset_service.get_by_id(asset_oid)
    except Exception as e:
        logger.exception(e)
        return '', 404

    # Make sure the Asset exists, is associated with the Set and has a state of `public`
    if not metadata or \
            str(metadata.get('set_id')) != str(set_item['_id']) or \
            metadata.get('state') != ASSET_STATES.PUBLIC:
        return '', 404

    try:
        binary = asset_service.download_binary(asset_oid)
    except Exception as e:
        logger.exception(e)
        return '', 404

    return construct_asset_download_response(metadata, binary)
