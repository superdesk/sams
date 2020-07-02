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

destinationSchema = {
    '_id': {
        'type': 'string',
        'unique': True
    },
    'provider': {
        'type': 'string'
    }
}
"""
**schema** =
    ``_id`` *string*
        Destination name
    ``provider`` *string*
        Destination's Provider name
"""
