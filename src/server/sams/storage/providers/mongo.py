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

"""MongoDB GridFS Storage Provider

In order for this provider to be available, MongoGridFSProvider needs to be added
to the list of STORAGE_PROVIDERS in your settings.py. For example::

    STORAGE_PROVIDERS = [
        'sams.storage.providers.mongo.MongoGridFSProvider'
    ]

This will then allow destinations to be configured for Sets to use. For example::

    STORAGE_DESTINATION_1 = 'MongoGridFS,Default,mongodb://localhost/sams'
"""

from typing import BinaryIO

from pymongo import MongoClient
from gridfs import GridFS
from gridfs.errors import NoFile
from bson import ObjectId

from .base import SamsBaseStorageProvider
from sams.errors import SuperdeskApiError


class MongoGridFSProvider(SamsBaseStorageProvider):
    """Provides storage to/from MongoDB GridFS

    :var pymongo.mongo_client.MongoClient _client: A client connected to a MongoDB Database
    :var gridfs.GridFS _fs: A client connected to a MongoDB GridFS Collection
    :var str type_name: The type name used to identify this provider - ``MongoGridFS``
    """

    type_name = 'MongoGridFS'

    def __init__(self, config_string: str):
        super(MongoGridFSProvider, self).__init__(config_string)

        self._client: MongoClient = None
        self._fs: GridFS = None

    def fs(self):
        """Returns the underlying GridFS client handle

        :return: A GridFS client to the configured database/collection
        :rtype: gridfs.GridFS
        """

        if self._fs is None:
            self._client = MongoClient(self.config_string)
            self._fs = GridFS(self._client.get_database())

        return self._fs

    def exists(self, asset_id: ObjectId) -> bool:
        """Checks if a file exists in the storage destination

        :param bson.objectid.ObjectId asset_id: The ID of the asset
        :return: ``True`` if a matching file exists, ``False`` otherwise
        :rtype: bool
        """

        return self.fs().exists(asset_id)

    def put(self, content: BinaryIO or bytes, filename: str) -> ObjectId:
        """Upload a file to the storage destination

        `content` must be an instance of :class:`bytes` or a file-like object
        providing a :meth:`read` method.

        :param bytes content: The data to be uploaded
        :param str filename: The filename
        :return: The ``"id"`` of the created file
        :rtype: bson.objectid.ObjectId
        """

        return self.fs().put(
            content,
            filename=filename
        )

    def get(self, asset_id: ObjectId):
        """Get an asset from the storage

        :param bson.objectid.ObjectId asset_id: The ID of the asset
        :return: A file-like object providing a :meth:`read` method
        :rtype: io.BytesIO
        """

        try:
            return self.fs().get(asset_id)
        except NoFile:
            raise SuperdeskApiError.notFoundError('Asset with id {} not found'.format(asset_id))

    def delete(self, asset_id: ObjectId):
        """Delete as asset from the storage

        :param bson.objectid.ObjectId asset_id: The ID of the asset
        """

        self.fs().delete(asset_id)

    def drop(self):
        """Deletes all assets from the storage"""

        self.fs()
        self._client.get_database().drop_collection('fs.files')
        self._client.get_database().drop_collection('fs.chunks')
