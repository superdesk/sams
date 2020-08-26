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

from importlib import import_module
from typing import Dict, List, Type

from sams_client.errors import SamsStorageProviderErrors

from .base import SamsBaseStorageProvider


class Provider:
    """A Provider instance

    :var str config_string: An entry from the ``STORAGE_PROVIDERS`` config attribute
    :var list[str] entries: The entries as provided by the config string
    :var str module_name: The name of the module, i.e. sams.storage.provider.mongo
    :var str class_name: The name of the class, i.e. MongoGridFSProvider
    :var module module: A reference to the loaded Python module
    :var type[SamsBaseStorageProvider] klass: A reference to the loaded Python class
    :var str type_name: The type_name as defined inside ``self.klass``
    """

    def __init__(self, config_string: str):
        """Initialise a new Provider instance

        :param str config_string: An entry from the ``STORAGE_PROVIDERS`` config attribute
        """

        self.config_string: str = config_string
        self.entries: List[str] = self.config_string.rsplit('.', 1)

        self.module_name: str = self.entries[0]
        self.class_name: str = self.entries[1]

        self.module = import_module(self.module_name)
        self.klass: Type[SamsBaseStorageProvider] = getattr(self.module, self.class_name)
        self.type_name: str = getattr(self.klass, 'type_name')

    def instance(self, config_string: str) -> SamsBaseStorageProvider:
        """Retrieve the StorageProvider instance for this provider

        :param str config_string: A string from any ``STORAGE_DESTINATION`` config attribute
        :return: A Storage Provider instance created from ``self.klass``,
         passing in the provided ``config_str``
        :rtype: SamsBaseStorageProvider
        """

        return self.klass(config_string)


class Providers:
    """A mechanism to register storage providers with the system

    This is used when bootstrapping the application to register storage
    providers from strings in the config.

    Usage::

        from sams.storage.providers import providers

        providers.register(...)
        providers.get(...)
        providers.exists(...)
        providers.all(...)
        providers.clear(...)
    """

    def __init__(self):
        self._providers: Dict[str, Provider] = dict()

    def register(self, config_str: str):
        """Register a provider with the system

        :param str config_str: The provider to add
        """

        provider = Provider(config_str)
        self._providers[provider.type_name] = provider

    def get(self, name: str) -> Provider:
        """Retrieve a registered storage provider by it's name

        :param str name: The name of the Provider
        :return: Returns the Provider instance
        :rtype: Provider
        :raises sams_client.errors.SamsStorageProviderErrors.NotFound: if the provider is not found
        """

        try:
            return self._providers[name]
        except KeyError:
            raise SamsStorageProviderErrors.NotFound(name)

    def exists(self, type_name: str) -> bool:
        """Check if a provider for the ``type_name`` exists

        :param type_name: The type name
        :returns: ``True`` if the provider is registered, ``False`` if not
        """

        return type_name in self._providers.keys()

    def all(self) -> Dict[str, Provider]:
        """Returns all the registered providers

        """

        return self._providers

    def clear(self):
        """Clears all of the registered providers

        """

        self._providers = {}


providers = Providers()
