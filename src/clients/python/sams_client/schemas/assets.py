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

from typing import NamedTuple, List, Dict, Any, Union
from typing_extensions import TypedDict
from datetime import datetime
from bson import ObjectId

from sams_client.utils import schema_relation, not_analyzed


class AssetStates(NamedTuple):
    """Named tuple for Asset states

    The state of an *Asset* defines the available actions on it.
    An *Asset* can be in any one of the following states:
    """

    #: Marks an Asset as not ready for use
    DRAFT: str
    #: Marks an Asset for internal use only
    INTERNAL: str
    #: Marks an Asset for public consumption
    PUBLIC: str


#: Asset states
ASSET_STATES: AssetStates = AssetStates('draft', 'internal', 'public')


class IAssetTag(TypedDict):
    """Tags that can be associated with an Asset"""

    #: String representing the unique id for this Tag
    code: str
    #: A human readable string for the Tag
    name: str


class IAssetRenditionArgs(TypedDict):
    """Arguments used when requesting a rendition to be created

    .. versionadded:: 0.3.0
    """

    #: Width of the image rendition
    width: int

    #: Height of the image rendition
    height: int

    #: Keep image's original aspect ratio
    keep_proportions: bool


class IAssetRendition(TypedDict):
    """Asset rendition metadata

    .. versionadded:: 0.3.0
    """

    # Name of this rendition
    name: str

    #: Internal media id (used by StorageProvider)
    _media_id: str

    #: Actual width of the image rendition
    width: int

    #: Actual height of the image rendition
    height: int

    #: Parameters used when this rendition was created
    params: IAssetRenditionArgs

    #: Date/time this rendition was created
    versioncreated: datetime

    #: Generated filename of this rendition
    filename: str

    #: Storage size of this rendition
    length: int


class IAsset(TypedDict):
    """Asset metadata"""

    #: Globally unique id, generated automatically by the system
    _id: Union[ObjectId, str]

    #: Globally unique id for the asset binary. This ID is generated by the StorageProvider
    _media_id: str

    #: A field to store the id of the user who uploaded the asset
    #:
    #: .. versionadded:: 0.2.0
    original_creator: str

    #: A field to store the id of the user who updated the asset
    #:
    #: .. versionadded:: 0.2.0
    version_creator: str

    #: A field to store time, when asset is created
    #:
    #: .. versionadded:: 0.2.0
    firstcreated: datetime

    #: A field to store time, when asset is updated
    #:
    #: .. versionadded:: 0.2.0
    versioncreated: datetime

    #: An auto-incrementing version field
    _version: int

    #: The ID of the Set where the Asset is to be stored
    set_id: ObjectId

    #: An optional ID of a parent Asset
    parent_id: ObjectId

    #: The state of the Asset (defaults to ``draft``). Can be one of ``draft``, ``internal`` or ``public``
    state: str

    #: The file name of the Asset Binary
    filename: str

    #: The size in bytes of the Asset Binary (calculated by the service)
    length: int

    #: The mimetype of the Asset Binary (calculated by the service)
    mimetype: str

    #: A name to give to the Asset
    name: str

    #: A short description describing the Asset
    description: str

    #: A list of code/name combinations so Assets can be grouped together through tags
    tags: List[IAssetTag]

    #: An extra dictionary to store further information about the Asset
    extra: Dict[str, Any]

    #: A special case attribute containing the actual binary data to be uploaded.
    #: This attribute will be removed from the metadata document before saving/updating
    binary: ObjectId

    #: If locked, ID of the external user who locked this asset
    #:
    #: .. versionadded:: 0.2.0
    lock_user: str

    #: If locked, ID of the exernal user session who locked this asset
    #:
    #: .. versionadded:: 0.2.0
    lock_session: str

    #: If locked, name of the action that for this lock (i.e. ``edit``)
    #:
    #: .. versionadded:: 0.2.0
    lock_action: str

    #: If locked, the date and time this asset was locked
    #:
    #: .. versionadded:: 0.2.0
    lock_time: datetime

    #: The list of renditions for this Asset (if it is an image)
    #:
    #: .. versionadded:: 0.3.0
    renditions: List[IAssetRendition]


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
    'renditions': {
        'type': 'list',
        'mapping': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                '_media_id': {
                    'type': 'string',
                    'index': 'not_analyzed',
                },
                'width': {'type': 'integer'},
                'height': {'type': 'integer'},
                'params': {
                    'type': 'object',
                    'properties': {
                        'width': {'type': 'integer'},
                        'height': {'type': 'integer'},
                        'keep_proportions': {'type': 'boolean'},
                    },
                },
                'versioncreated': {'type': 'date'},
                'filename': {'type': 'string'},
                'length': {'type': 'long'},
            }
        }
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
