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

from superdesk import get_backend
from .storage_destinations import StorageDestinationsResource, StorageDestinationsService


def init_app(app):
    _service = StorageDestinationsService(StorageDestinationsResource.endpoint_name, backend=get_backend())
    StorageDestinationsResource(
        endpoint_name=StorageDestinationsResource.endpoint_name,
        app=app,
        service=_service
    )
