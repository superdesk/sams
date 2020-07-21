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

from superdesk.resource import Resource
from sams_client.schemas import ASSET_SCHEMA


class AssetsResource(Resource):
    endpoint_name = resource_title = 'assets'
    url = '/internal/assets'
    internal_resource = True
    schema = ASSET_SCHEMA

    datasource = {
        'source': 'assets',
        'search_backend': 'elastic'
    }
    mongo_indexes = {
        'media_ids': [('_media_id', 1)]
    }
