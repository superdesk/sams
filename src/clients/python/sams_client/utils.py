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
from typing import Dict, any, Tuple


def load_configs(configs: Dict):
    """Load host, port from configs

    :param dict configs: Dictionary of configuration for server's host and port
    :rtype: tuple
    :return: A tuple containing host and port
    """
    host = configs.get('HOST', DEFAULT_HOST)
    port = configs.get('PORT', DEFAULT_PORT)

    return host, port


def get_base_url(configs: Dict):
    """Load configs and return base url

    :param dict configs: Dictionary of configuration for server's host and port
    :rtype: str
    :return: Base url consisting of protocol, host and port
    """
    host, port = load_configs(configs)
    return f'{DEFAULT_PROTOCOL}://{host}:{port}'
