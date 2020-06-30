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


"""
Usage
-----
The StorageDestinationsService instance can be found under :data:`sams.api.admin` and used as::

    from sams.api.admin import get_service

    def test_storage_destinations():
        storage_destinations_service = get_service()

        sets_service.get()
        sets_service.find_one({...})

This service instance can only be used after the application has bootstrapped.
"""

from superdesk import get_backend
from .storage_destinations import StorageDestinationsResource, StorageDestinationsService

_service: StorageDestinationsService


def get_service() -> StorageDestinationsService:
    return _service

def init_app(app):
    _service = StorageDestinationsService(StorageDestinationsResource.endpoint_name, backend=get_backend())
    StorageDestinationsResource(
        endpoint_name=StorageDestinationsResource.endpoint_name,
        app=app,
        service=_service
    )
