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

from typing import NamedTuple

from sams_client.utils import schema_relation, not_analyzed


#: Asset states
class AssetStates(NamedTuple):
    DRAFT: str
    INTERNAL: str
    PUBLIC: str


ASSET_STATES: AssetStates = AssetStates('draft', 'internal', 'public')
"""
The state of an *Asset* defines the available actions on it.
An *Asset* can be in any one of the following states:

* **DRAFT:** Marks an Asset as not ready for use

* **INTERNAL:** Marks an Asset for internal use only

* **PUBLIC:** Marks an Asset for public consumption
"""


ASSET_SCHEMA = {
    '_media_id': {
        'type': 'string',
        'mapping': not_analyzed
    },
    'original_creator': {
        'type': 'string',
        'mapping': not_analyzed
    },
    'version_creator': {
        'type': 'string',
        'mapping': not_analyzed
    },
    'firstcreated': {
        'type': 'datetime'
    },
    'versioncreated': {
        'type': 'datetime'
    },
    '_version': {
        'type': 'number'
    },
    'set_id': schema_relation('sets', required=True),
    'parent_id': schema_relation('assets'),
    'state': {
        'type': 'string',
        'allowed': tuple(ASSET_STATES),
        'default': ASSET_STATES.DRAFT,
        'nullable': False,
        'mapping': not_analyzed
    },
    'filename': {
        'type': 'string',
        'required': True,
        'mapping': {
            'type': 'text',

            # Use the `filename_analyzer` to tokenize filenames
            # i.e. tokenizes
            # `bbb_0001.png`
            # to
            # [`bbb`, `0001`, `png`]
            'analyzer': 'filename_analyzer',
            'search_analyzer': 'filename_analyzer',

            # Keep field data in case we need aggregations
            # on each token, otherwise aggregate against `filename.keyword`
            'fielddata': True,

            # Add subtype `keyword` so that we can sort by `name`
            'fields': {
                'keyword': {
                    'type': 'keyword',
                    'ignore_above': 256
                }
            }
        }
    },
    'length': {
        'type': 'integer',
        'mapping': {
            'type': 'long'
        }
    },
    'mimetype': {
        'type': 'string',
        'mapping': not_analyzed
    },
    'name': {
        'type': 'string',
        'required': True,
        'nullable': False,
        'empty': False,
        'mapping': {
            'type': 'text',

            # Use the `filename_analyzer` to tokenize names
            # i.e. tokenizes
            # `bbb_0001.png`
            # to
            # [`bbb`, `0001`, `png`]
            'analyzer': 'filename_analyzer',
            'search_analyzer': 'filename_analyzer',

            # Keep field data in case we need aggregations
            # on each token, otherwise aggregate against `name.keyword`
            'fielddata': True,

            # Add subtype `keyword` so that we can sort by `name`
            'fields': {
                'keyword': {
                    'type': 'keyword',
                    'ignore_above': 256
                }
            }
        }
    },
    'description': {
        'type': 'string'
    },
    'tags': {
        'type': 'list',
        'nullable': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'code': {
                    'type': 'string',
                    'required': True,
                    'mapping': not_analyzed
                },
                'name': {
                    'type': 'string',
                    'required': True,
                    'mapping': not_analyzed
                }
            }
        },
    },
    'extra': {
        'type': 'dict',
        'schema': {},
        'allow_unknown': True
    },
    'binary': {
        'type': 'media',
        'mapping': not_analyzed
    },
    'lock_user': {
        'type': 'string',
        'mapping': not_analyzed,
        'required': False,
        'nullable': True,
        'empty': True
    },
    'lock_session': {
        'type': 'string',
        'mapping': not_analyzed,
        'required': False,
        'nullable': True,
        'empty': True
    },
    'lock_action': {
        'type': 'string',
        'mapping': not_analyzed,
        'required': False,
        'nullable': True,
        'empty': True
    },
    'lock_time': {
        'type': 'datetime',
        'required': False,
        'nullable': True,
        'empty': True
    }
}
"""
**Schema** =
    ``_id`` *bson.objectid.ObjectId*
        Globally unique id, generated automatically by the system
    ``_media_id`` *string*
        Globally unique id for the asset binary. This ID is generated by the StorageProvider
    ``original_creator`` *string*
        A field to store the id of the user who uploaded the asset
    ``version_creator`` *string*
        A field to store the id of the user who updated the asset
    ``firstcreated`` *string*
        A field to store time, when asset is created
    ``versioncreated`` *string*
        A field to store time, when asset is updated
    ``_version`` *int*
        An auto-incrementing version field
    ``set_id`` *bson.objectid.ObjectId*
        The ID of the Set where the Asset is to be stored
    ``parent_id`` *bson.objectid.ObjectId*
        An optional ID of a parent Asset
    ``state`` *string*
        The state of the Asset (defaults to ``draft``). Can be one of ``draft``, ``internal`` or ``public``
    ``filename`` *string*
        The file name of the Asset Binary
    ``length`` *int*
        The size in bytes of the Asset Binary (calculated by the service)
    ``mimetype`` *string*
        The mimetype of the Asset Binary (calculated by the service)
    ``name`` *string*
        A name to give to the Asset
    ``description`` *string*
        A short description describing the Asset
    ``tags`` *list[dict]*
        A list of code/name combinations so Assets can be grouped together through tags
    ``extra`` *dict*
        An extra dictionary to store further information about the Asset
    ``binary`` *io.BytesIO*
        A special case attribute containing the actual binary data to be uploaded.
        This attribute will be removed from the metadata document before saving/updating
"""
