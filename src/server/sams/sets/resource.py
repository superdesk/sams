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

from collections import namedtuple
from superdesk.resource import Resource


# set states
set_states = ['draft', 'usable', 'disabled']
SET_STATES = namedtuple(
    'SET_STATE',
    ['DRAFT', 'USABLE', 'DISABLED']
)(*set_states)


class SetsResource(Resource):
    endpoint_name = resource_title = 'sets'
    url = 'internal/sets'

    internal_resource = True

    schema = {
        'name': {
            'type': 'string',
            'required': True,
            'nullable': False,
            'empty': False,
            'unique': True
        },
        'state': {
            'type': 'string',
            'allowed': set_states,
            'default': SET_STATES.DRAFT,
            'nullable': False
        },
        'description': {
            'type': 'string'
        },
        'destination_name': {
            'type': 'string',
            'required': True
        },
        'destination_config': {
            'type': 'dict',
            'schema': {},
            'allow_unknown': True,
        }
    }
