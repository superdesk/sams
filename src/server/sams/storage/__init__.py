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

from sams.default_settings import env
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

    # Load the storage destinations from either app.config or env variables
    while True:
        destination_id = config_entry_template.format(config_id)
        if destination_id not in app.config:
            env_val = env(destination_id)
            if not env_val:
                break

            app.config[destination_id] = env_val
        destinations.register(app.config[destination_id])
        config_id += 1
