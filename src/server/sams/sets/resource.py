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
"""
The state of a *Set* defines the available actions on it. \
A *Set* can be in any one of the following states:

* **DRAFT:** allows the administrator to configure the *Set* \
with the correct ``destination_name`` and ``destination_config``.

    * ``destination_name`` can be changed
    * ``destination_config`` can be changed
    * The *Set* can be deleted
    * *Assets* **cannot** be uploaded to it
    * *Assets* **cannot** be downloaded from it

* **USABLE:** Once the administrator has completed configuring \
the *Set*, they will change the ``state`` to ``usable``. This \
means ``producers`` can now upload *Assets* to the *Set*.

    * ``destination_name`` **cannot** be changed
    * ``destination_config`` **cannot** be changed
    * The *Set* **cannot** be deleted
    * The ``state`` can only be changed to ``disabled``
    * *Assets* can be uploaded to it
    * *Assets* can be downloaded from it

* **DISABLED:** The administrator is able to change a *Set* to \
be in disabled, so ``producers`` are unable to add new *Assets* to it.

    * ``destination_name`` **cannot** be changed
    * ``destination_config`` **cannot** be changed
    * The *Set* **cannot** be deleted
    * The ``state`` can only be changed to ``usable``
    * *Assets* **cannot** be uploaded to it
    * *Assets* can be downloaded from it

.. note::
    The attributes ``destination_name`` and ``destination_config`` \
    are read-only when the ``state`` is ``usable`` or ``disabled``.\
    This is because the system would have to move *Assets* to \
    the new destination, which would be better suited to a migrate endpoint.
"""


class SetsResource(Resource):
    """
    **schema** =
        ``_id`` *bson.ObjectId*
            Globally unique id, generated automatically by the system.
        ``state`` *string*
            The state of the Set. One of ``draft``, ``usable``, or ``disabled``.
        ``name`` *string*
            Unique name for the Set
        ``description`` *string*
            A short description on what this set is designated for
        ``destination_name`` *string*
            The name of a registered StorageDestination (:mod:`sams.storage.destinations`)
        ``destination_config`` *dict*
            A dictionary containing the configuration options for the specific destination used
    """

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
