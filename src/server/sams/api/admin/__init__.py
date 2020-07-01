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

from sams.factory.app import SamsApp
from sams.sets import get_service
from .sets import AdminSetResource, AdminSetService


def init_app(app: SamsApp):
    AdminSetResource(
        endpoint_name=AdminSetResource.endpoint_name,
        app=app,
        service=AdminSetService(get_service())
    )
