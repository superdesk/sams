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

This provider is enabled by default in the ``STORAGE_PROVIDERS`` config.
If you need to override this default, make sure to include MongoGridFSProvider.
For example::

    STORAGE_PROVIDERS = [
        'sams.storage.providers.mongo.MongoGridFSProvider'
    ]

This will then allow destinations to be configured for Sets to use. For example::

    STORAGE_DESTINATION_1 = 'MongoGridFS,Default,mongodb://localhost/sams'
"""

from typing import BinaryIO, Union

from pymongo import MongoClient
from gridfs import GridFS
from gridfs.errors import NoFile
from gridfs.grid_file import GridOut, EMPTY
from bson import ObjectId

from superdesk.storage.superdesk_file import SuperdeskFile

from .base import SamsBaseStorageProvider
from sams_client.errors import SamsAssetErrors


class GridfsFileWrapper(SuperdeskFile):
    """SuperdeskFile implementation for GridFS files"""

    def __init__(self, gridfs_file: GridOut):
        super().__init__()

        blocksize = 65636
        buf = gridfs_file.read(blocksize)
        while buf != EMPTY:
            self.write(buf)
            buf = gridfs_file.read(blocksize)

        self.seek(0)
        self.content_type = gridfs_file.content_type
        self.length = gridfs_file.length
        self._name = gridfs_file.name
        self.filename = gridfs_file.filename
        self.metadata = gridfs_file.metadata
        self.upload_date = gridfs_file.upload_date
        self.md5 = gridfs_file.md5
        self._id = gridfs_file._id


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

    def fs(self) -> GridFS:
        """Returns the underlying GridFS client handle

        :return: A GridFS client to the configured database/collection
        :rtype: gridfs.GridFS
        """

        if self._fs is None:
            self._client = MongoClient(self.config_string)
            self._fs = GridFS(self._client.get_database())

        return self._fs

    def exists(self, media_id: Union[ObjectId, str]) -> bool:
        """Checks if a file exists in the storage destination

        :param bson.objectid.ObjectId media_id: The ID of the asset
        :return: ``True`` if a matching file exists, ``False`` otherwise
        :rtype: bool
        """

        if isinstance(media_id, str):
            media_id = ObjectId(media_id)

        return self.fs().exists(media_id)

    def put(self, content: Union[BinaryIO, bytes], filename: str, mimetype: str = None) -> str:
        """Upload a file to the storage destination

        `content` must be an instance of :class:`bytes` or a file-like object
        providing a :meth:`read` method.

        :param bytes content: The data to be uploaded
        :param str filename: The filename
        :param str mimetype: The mimetype of the content (not used here)
        :return: The ``"id"`` of the created file
        :rtype: str
        """

        media_id = self.fs().put(
            content,
            filename=filename
        )
        return str(media_id)

    def get(self, media_id: Union[ObjectId, str]) -> GridfsFileWrapper:
        """Get an asset from the storage

        :param bson.objectid.ObjectId media_id: The ID of the asset
        :return: A file-like object providing a :meth:`read` method
        :rtype: io.BytesIO
        """

        if isinstance(media_id, str):
            media_id = ObjectId(media_id)

        try:
            gridfs_file = self.fs().get(media_id)
            if gridfs_file:
                return GridfsFileWrapper(gridfs_file)
        except NoFile:
            raise SamsAssetErrors.AssetNotFound(media_id)

    def delete(self, media_id: Union[ObjectId, str]):
        """Delete as asset from the storage

        :param bson.objectid.ObjectId media_id: The ID of the asset
        """

        if isinstance(media_id, str):
            media_id = ObjectId(media_id)

        self.fs().delete(media_id)

    def drop(self):
        """Deletes all assets from the storage"""

        self.fs()
        self._client.get_database().drop_collection('fs.files')
        self._client.get_database().drop_collection('fs.chunks')
