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
from sams_client.schemas import SET_SCHEMA


class SetsResource(Resource):
    """
    **schema** =
        ``_id`` *bson.objectid.ObjectId*
            Globally unique id, generated automatically by the system.
        ``state`` *string* (:mod:`sams_client.schemas.sets.SET_STATES`)
            The state of the Set. One of ``draft``, ``usable``, or ``disabled``.
        ``name`` *string*
            Unique name for the Set
        ``description`` *string*
            A short description on what this set is designated for
        ``destination_name`` *string*
            The name of a registered StorageDestination (:mod:`sams.storage.destinations`)
        ``destination_config`` *dict*
            A dictionary containing the configuration options for the specific destination used
        ``maximum_asset_size`` *long*
            The maximum size of an Asset that can be uploaded to this Set (optional)
    """

    endpoint_name = resource_title = 'sets'
    url = 'internal/sets'

    internal_resource = True

    schema = SET_SCHEMA
