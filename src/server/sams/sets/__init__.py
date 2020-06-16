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
from .resource import SetsResource
from .service import SetsService


service: SetsService
"""
The Set service instance can be found under :data:`sams.sets.service` and used all::

    from sams.sets import service as sets_service

    def test_sets():
        sets_service.post([{....}])
        sets_service.patch(set_id, {...})
        sets_service.delete_action({...})
        sets_service.find({...})

This service instance can only be used after the application has bootstrapped.
"""


def init_app(app):
    global service

    service = SetsService(SetsResource.endpoint_name, backend=get_backend())
    SetsResource(
        endpoint_name=SetsResource.endpoint_name,
        app=app,
        service=service
    )
