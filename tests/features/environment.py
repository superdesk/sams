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

from tests.features.steps.app import get_app
from tests.server.utils import get_test_db_host


def before_all(context):
    setattr(context, 'DB_HOST', get_test_db_host())
    get_app(context).start()


def before_scenario(context, scenario):
    get_app(context).prepopulate([{'method': 'reset'}])


def after_scenario(context, scenario):
    try:
        if context._reset_after_scenario:
            app = get_app(context)
            app.init()
            app.start()
            context.app = app
            context._reset_after_scenario = False
    except KeyError:
        pass


def after_all(context):
    get_app(context).stop()
