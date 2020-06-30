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

from sams.factory.service import SamsService
from sams.storage.destinations import destinations
from superdesk.resource import Resource
from sams_client.schemas import destinationSchema
from superdesk.utils import ListCursor


class StorageDestinationsResource(Resource):
    """Resource instance for Storage Destinations
    """

    endpoint_name = 'destinations'
    url = 'admin/destinations'
    item_url = r'regex("[a-zA-Z0-9]+")'

    schema = destinationSchema

    item_methods = ['GET']
    resource_methods = ['GET']


class StorageDestinationsService(SamsService):
    """Service for storage destinations

    Returns one or all registered storage destinations
    """

    def get(self, req, **lookup):
        """
        Returns a list of all the registered storage destinations
        """
        return ListCursor(list(map(
            lambda destination: destination.to_dict(),
            destinations.all().values()
        )))

    def find_one(self, req, **lookup):
        """
        Uses _id in the lookup and returns the destination
        name and provider name of the respective storage destination
        """
        name = lookup['_id']
        destination = destinations.get(name)
        response = destination.to_dict()
        return response
