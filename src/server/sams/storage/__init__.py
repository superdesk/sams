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


from .providers import providers
from .destinations import destinations


def init_app(app: SamsApp):
    providers.clear()
    destinations.clear()

    for provider in app.config.get('STORAGE_PROVIDERS') or []:
        providers.register(provider)

    config_entry_template = 'STORAGE_DESTINATION_{}'
    config_id = 1

    while config_entry_template.format(config_id) in app.config:
        destinations.register(app.config[config_entry_template.format(config_id)])
        config_id += 1
