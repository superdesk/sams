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

from typing import Dict, Any, List
from requests import Response

from superdesk.default_settings import env

import sams_client.default_settings as default_config
from .constants import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_PROTOCOL

not_analyzed = {'type': 'string', 'index': 'not_analyzed'}


def load_config(config: Dict[str, Any]) -> Dict[str, str]:
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
) -> Dict[str, Any]:
    """Creates an Eve/Cerberus relation attribute

    This is copied from superdesk.resource.rel so that we don't have to
    import Superdesk-Core for the sams_client library

    :param str resource: The name of the resource
    :param bool embeddable: If the relation can be embedded when fetching
    :param bool required: If this relation is required, for validation purposes
    :param str data_type: The data type to apply to the schema, defaults to 'objectid'
    :param bool nullable: If this relation can have a ``null`` value
    :param bool readonly: If this relation is read-only
    :return: A dictionary to apply to a Resource schema
    :rtype: dict
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


def bytes_to_human_readable(size: int) -> str:
    """Converts size in bytes to a human readable string

    Converts the integer provided into one of the following:
        * ``'x bytes'``
        * ``'x.yy KB'`` (to 2 decimal places)
        * ``'x.yy MB'`` (to 2 decimal places)

    :param int size: Size in bytes to convert
    :return: A human readable string
    :rtype: int
    """

    if size < 1024:
        return f'{size} bytes'
    elif size < 1048576:
        return f'{size / 1024:.2f} KB'
    else:
        return f'{size / 1048576:.2f} MB'


def get_aggregation_buckets(response: Response, bucket_name: str) -> List[Dict[str, Any]]:
    """Utility function to get aggregation buckets

    :param requests.Response response: The response object from the API call
    :param str bucket_name: The name of the bucket to retrieve
    :return: The list of buckets from the aggregation query
    :rtype: list
    """

    json = response.json()
    return ((json.get('_aggregations') or {}).get(bucket_name) or {}).get('buckets') or []
