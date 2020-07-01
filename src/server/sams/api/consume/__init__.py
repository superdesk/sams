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
from .sets import ConsumeSetResource, ConsumeSetService


def init_app(app: SamsApp):
    ConsumeSetResource(
        endpoint_name=ConsumeSetResource.endpoint_name,
        app=app,
        service=ConsumeSetService(get_service())
    )
