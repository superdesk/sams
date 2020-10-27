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

"""Storage Provider base is a.....

The :mod:`sams.storage.providers.base` package provides storage io implementations.

"""

from typing import Union, BinaryIO

from bson import ObjectId

from superdesk.storage.superdesk_file import SuperdeskFile

from sams_client.errors import SamsConfigErrors


class SamsBaseStorageProvider(object):
    """An instance of SamsBaseStorageProvider
    """

    type_name: str = None
    name: str = None
    config_string: str = None

    def __init__(self, config_string: str):
        """Creates a new instance of :class:`SamsBaseStorageProvider`.

        This is the base class that storage implementations must inherit from.

        :param str config_string: A string from any ``STORAGE_DESTINATION`` config attribute
        """

        self.process_config_string(config_string)

    def process_config_string(self, config_string: str):
        """Extract relevant information from the provided ``config_string``

        :param str config_string: A string from any ``STORAGE_DESTINATION`` config attribute
        :raises ValueError: If there
        """

        if config_string is None:
            raise SamsConfigErrors.StorageProviderConfigStringNotProvided()

        config_parts = config_string.split(',', 2)

        if len(config_parts) != 3:
            raise SamsConfigErrors.StorageProviderIncorrectConfigArguments(len(config_parts))

        if config_parts[0] != self.type_name:
            raise SamsConfigErrors.StorageProviderInvalidConfig(self.type_name, config_parts[0])

        self.name = config_parts[1]
        self.config_string = config_parts[2]

    def exists(self, media_id: Union[ObjectId, str]) -> bool:
        """Checks if a file exists in the storage destination

        This method *must* be defined in the derived class

        :param media_id: The ID of the asset
        :return: ``True`` if a matching file exists, ``False`` otherwise
        :raises NotImplementedError: If not defined in derived class
        """

        raise NotImplementedError()

    def put(self, content: Union[BinaryIO, str], filename: str, mimetype: str = None) -> str:
        """Upload a file to the storage destination

        `content` must be an instance of :class:`bytes` or a file-like object
        providing a :meth:`read` method.

        This method *must* be defined in the derived class

        :param bytes content: The data to be uploaded
        :param str filename: The filename
        :param str mimetype: The mimetype of the content
        :return: The ``"id"`` of the created file
        :raises NotImplementedError: If not defined in derived class
        """

        raise NotImplementedError()

    def get(self, media_id: Union[ObjectId, str]) -> SuperdeskFile:
        """Get an asset from the storage

        This method *must* be defined in the derived class

        :param media_id: The ID of the asset
        :return:
        :raises NotImplementedError: If not defined in derived class
        """

        raise NotImplementedError()

    def delete(self, media_id: Union[ObjectId, str]):
        """Delete as asset from the storage

        This method *must* be defined in the derived class

        :param media_id: The ID of the asset
        :raises NotImplementedError: If not defined in derived class
        """

        raise NotImplementedError()

    def drop(self):
        """Deletes all assets from the storage

        This method *must* be defined in the derived class

        :raises NotImplementedError: If not defined in derived class
        """

        raise NotImplementedError()
