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

from .constants import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_PROTOCOL


def load_configs(configs):
    """Load host, port from configs
    """
    host = configs.get('HOST', DEFAULT_HOST)
    port = configs.get('PORT', DEFAULT_PORT)

    return host, port


def get_base_url(configs):
    """Load configs and return base url
    """
    host, port = load_configs(configs)
    return f'{DEFAULT_PROTOCOL}://{host}:{port}'
