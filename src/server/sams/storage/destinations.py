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

from typing import Dict, List

from sams_client.errors import SamsStorageDestinationErrors

from .providers import Provider, providers
from .providers.base import SamsBaseStorageProvider


class Destination:
    """A Destination instance

    :var str config_string: A string from any ``STORAGE_DESTINATION`` config attribute
    :var list[str] entries: The entries as provided by the ``config_string``
    :var str name: The name of the destination
    :var str provider_name: The name of the provider
    :var Provider provider: The provider instance
    :var str config: The config part from the ``entries``
    """

    def __init__(self, config_str: str):
        """Initialise a new Destination instance

        :param str config_str: The config string from settings.py
        """

        self.config_string: str = config_str

        self.entries: List[str] = self.config_string.split(',', 2)

        self.name: str = self.entries[1]
        self.provider_name: str = self.entries[0]
        self.config: str = self.entries[2]

        self.provider: Provider = providers.get(self.provider_name)

    def provider_instance(self) -> SamsBaseStorageProvider:
        """Retrieve the Storage instance for this destination

        :return: An Storage Provider instance
        :rtype: SamsBaseStorageProvider
        """

        return self.provider.instance(self.config_string)

    def to_dict(self):
        """Return a dictionary containing name and provider

        :return: A dictionary containing name and provider_name of destination
        :rtype: dict
        """
        return {
            '_id': self.name,
            'provider': self.provider_name
        }


class Destinations:
    """A mechanism to register storage destinations with the system

    This is used when bootstrapping the application to register storage
    destinations from strings in the config.

    Usage::

        from sams.storage.destinations import destinations

        destinations.register(...)
        destinations.get(...)
        destinations.exists(...)
        destinations.all(...)
        destinations.clear(...)
    """

    def __init__(self):
        self._destinations: Dict[str, Destination] = dict()

    def register(self, config_string: str):
        """Register a storage destination with the system

        :param str config_string: A string from any ``STORAGE_DESTINATION`` config attribute
        """

        destination = Destination(config_string)
        self._destinations[destination.name] = destination

    def get(self, name: str) -> Destination:
        """Retrieve a registered storage destination by it's name

        :param str name: The name of the storage destination
        :return: Returns the Destination instance
        :rtype: Destination
        :raises sams_client.errors.SamsStorageDestinationErrors.NotFound: if the destination is not found
        """

        try:
            return self._destinations[name]
        except KeyError:
            raise SamsStorageDestinationErrors.NotFound(name)

    def exists(self, name: str) -> bool:
        """Check if a storage destination with ``name`` exists

        :param str name: The name of the storage destination
        :returns: ``True`` if the destination exists, ``False`` if not
        """

        return name in self._destinations.keys()

    def all(self) -> Dict[str, Destination]:
        """Returns all the registered storage destinations"""

        return self._destinations

    def clear(self):
        """Clears all of the registered storage destinations"""

        self._destinations = {}


destinations = Destinations()
