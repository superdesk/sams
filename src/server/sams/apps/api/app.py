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

from typing import Dict, Any, Optional

from sams.factory.app import SamsApp


def get_app(import_name: Optional[str] = __package__, config: Optional[Dict[str, Any]] = None) -> SamsApp:
    """Creates and returns a new instance of the SAMS API application

    **Default integrated apps**::

        CORE_APPS = [
            'sams.sets',
            'sams.storage',
            'sams.assets',
            'sams.commands'
        ]

        INSTALLED_APPS = [
            'sams.factory.sentry',
            'sams.api.admin',
            'sams.api.consume',
            'sams.api.produce'
        ]

    :param str import_name: Optional name to use for this application (defaults to ``__package__``)
    :param dict config: Optional config overrides
    :return: SAMS API application instance
    :rtype: sams.factory.app.SamsApp
    """

    return SamsApp(import_name=import_name, config=config)
