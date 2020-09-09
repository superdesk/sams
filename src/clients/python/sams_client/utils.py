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

from typing import Dict

from superdesk.default_settings import env

import sams_client.default_settings as default_config
from .constants import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_PROTOCOL

not_analyzed = {'type': 'string', 'index': 'not_analyzed'}


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


def schema_relation(
    resource: str,
    embeddable: bool = True,
    required: bool = False,
    data_type: str = 'objectid',
    nullable: bool = False,
    readonly: bool = False
):
    """Creates an Eve/Cerberus relation attribute

    This is copied from superdesk.resource.rel so that we don't have to
    import Superdesk-Core for the sams_client library
    """

    return {
        'type': data_type,
        'required': required,
        'nullable': nullable,
        'readonly': readonly,
        'data_relation': {
            'resource': resource,
            'field': '_id',
            'embeddable': embeddable
        },
        'mapping': {'type': 'keyword'},
    }
