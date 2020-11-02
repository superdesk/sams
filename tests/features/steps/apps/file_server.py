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

from typing import Dict, Any

from sams.apps.file_server.settings import INSTALLED_APPS
from sams.apps.file_server.app import get_app

from sams_client import SamsClient

from .base import BaseTestApp


class TestFileServer(BaseTestApp):
    def get_config(self) -> Dict[str, Any]:
        return {
            'INSTALLED_APPS': INSTALLED_APPS,
            'SERVER_NAME': 'localhost:5750'
        }

    def get_app(self, config: Dict[str, Any]):
        return get_app('sams_file_server', config=config)


def get_file_server(context) -> TestFileServer:
    try:
        app = getattr(context, 'app_file_server')
    except AttributeError:
        app = TestFileServer()
        app.init()
        context.app_file_server = app

    return app


def get_file_server_client(context) -> SamsClient:
    return get_file_server(context).client
