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
from json import dumps

from superdesk.default_settings import env

import sams_client.default_settings as default_config
from .constants import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_PROTOCOL


def load_config(config: Dict):
    """Load host, port from config

    :param dict config: Dictionary of configuration provided
    :rtype: dict
    :return: A dictionary containing base_url, auth_type and auth_key
    """
    host = config.get('HOST', DEFAULT_HOST)
    port = config.get('PORT', DEFAULT_PORT)

    return {
        'base_url': f'{DEFAULT_PROTOCOL}://{host}:{port}',
        'auth_type': config.get(
            'SAMS_AUTH_TYPE', default_config.SAMS_AUTH_TYPE
        ),
        'auth_key': config.get(
            'SAMS_AUTH_KEY', env('SAMS_AUTH_KEY', '')
        )
    }


def urlencode(url: str, args: Dict[str, Any] = None) -> str:
    """Generates a url with a query string included

    Uses :meth:`json.dumps` to convert arg values to strings.
    This is required as the urllib.parse.urlencode uses single quotes
    where as Eve raises an exception unless double quotes are used.

    :param str url: The base url
    :param dict args: Dictionary containing query arguments
    :rtype: str
    :return: The full url including the query string
    """

    if not args:
        return url

    query_string = '?' + '&'.join([
        '{}={}'.format(
            key,
            dumps(val)
        )
        for key, val in args.items()
    ])

    return url + query_string
