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

from superdesk import get_backend, get_resource_service
from .resource import SetsResource
from .service import SetsService


service: SetsService


def init_app(app):
    global service

    service = SetsService(SetsResource.endpoint_name, backend=get_backend())
    SetsResource(
        endpoint_name=SetsResource.endpoint_name,
        app=app,
        service=service
    )
