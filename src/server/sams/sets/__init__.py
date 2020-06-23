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

"""A set a collection of *Assets*. It is used as a way to organise and restrict access to
the *Assets* it holds.

All access to the binary or metadata of assets will go through this service. There must
be at least one Set configured in the system.

A single Set can be designated as the default Set. When access is requested to an asset
without a set being provided, the default set will be used.

Usage
-----
The Set service instance can be found under :data:`sams.sets.service` and used all::

    from sams.sets import get_service

    def test_sets():
        sets_service = get_service()

        sets_service.post([{....}])
        sets_service.patch(set_id, {...})
        sets_service.delete_action({...})
        sets_service.find({...})

This service instance can only be used after the application has bootstrapped.
"""

from superdesk import get_backend
from .resource import SetsResource
from .service import SetsService


_service: SetsService


def get_service() -> SetsService:
    return _service


def init_app(app):
    global _service

    _service = SetsService(SetsResource.endpoint_name, backend=get_backend())
    SetsResource(
        endpoint_name=SetsResource.endpoint_name,
        app=app,
        service=_service
    )
