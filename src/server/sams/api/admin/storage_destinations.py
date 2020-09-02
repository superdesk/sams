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

"""The Destinations Admin API allows to retrieve the list of ``StorageDestinations``.

This service and resource is intended to be used by external clients.
To access ``StorageDestinations`` inside the SAMS application,
use the :mod:`sams.storage.destinations` module instead.

=====================   =================================================================
**endpoint name**        'admin_destinations'
**resource title**       'Destinations'
**resource url**         [GET] '/admin/destinations'
**item url**             [GET] '/admin/destinations/<:class:`str`>'
**schema**               :attr:`sams_client.schemas.destinations.destinationSchema`
=====================   =================================================================
"""

from sams.factory.service import SamsService
from sams.storage.destinations import destinations
from superdesk.resource import Resource
from superdesk.utils import ListCursor


class StorageDestinationsResource(Resource):
    """Resource instance for Storage Destinations

    **schema** =
        ``_id`` *string*
            Destination name
        ``provider`` *string*
            Destination's Provider name
    """

    endpoint_name = 'destinations'
    url = 'admin/destinations'
    item_url = r'regex("[a-zA-Z0-9]+")'
    item_methods = ['GET']
    resource_methods = ['GET']
    allow_unknown = True


class StorageDestinationsService(SamsService):
    """Service for storage destinations

    Returns one or all registered storage destinations
    """

    def get(self, req, **lookup):
        """
        Returns a list of all the registered storage destinations
        sorted alphabetically by '_id'
        """
        destinationsList = list(map(
            lambda destination: destination.to_dict(),
            destinations.all().values()
        ))
        destinationsList.sort(key=lambda x: x['_id'])
        return ListCursor(destinationsList)

    def find_one(self, req, **lookup):
        """
        Uses ``_id`` in the lookup and returns the destination
        name and provider name of the respective storage destination
        """
        name = lookup['_id']
        destination = destinations.get(name)
        response = destination.to_dict()
        return response
