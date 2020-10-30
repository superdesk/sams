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

from tests.features.steps.apps.api import get_api
from tests.features.steps.apps.file_server import get_file_server
from tests.server.utils import get_test_db_host, get_test_storage_destinations


def before_all(context):
    setattr(context, 'DB_HOST', get_test_db_host())
    setattr(context, 'STORAGE_PROVIDER', {'type': get_test_storage_destinations()[0].split(',')[0]})
    get_api(context).start()
    get_file_server(context).start()


def before_scenario(context, scenario):
    get_api(context).prepopulate([{'method': 'reset'}])


def after_scenario(context, scenario):
    try:
        if context._reset_after_scenario:
            api = get_api(context)
            api.init()
            api.start()
            context.app_api = api

            file_server = get_file_server(context)
            file_server.init()
            file_server.start()
            context.app_file_server = file_server

            context._reset_after_scenario = False
    except KeyError:
        pass


def after_all(context):
    get_api(context).stop()
    get_file_server(context).stop()
