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

from copy import deepcopy
from bson import ObjectId

from sams_client.schemas import SET_STATES

from sams.factory.service import SamsService
from sams.storage.destinations import Destination, destinations
from sams.storage.providers.base import SamsBaseStorageProvider
from sams_client.errors import SamsSetErrors


class SetsService(SamsService):
    def validate_post(self, doc):
        """Validates the Set on creation

        The following additional validation is performed on Sets being created:
            * The ``destination_name`` must exist in a ``STORAGE_DESTINATION_`` config attribute

        :param doc: The provided document to validate
        :raises Superdesk.validation.ValidationError: If there are validation errors
        """

        super().validate_post(doc)
        self._validate_destination_name(doc)

    def validate_patch(self, original, updates):
        """Validates the Set on update

        The following additional validation is performed on Sets being updated:
            * Once a set has changed from ``draft`` state, it can never return to ``draft``
            * Once a set has changed from ``draft`` state, ``destination_name`` and \
            ``destination_config`` cannot be changed
            * The ``destination_name`` must exist in a ``STORAGE_DESTINATION_`` config attribute

        :param original: The original document from the database
        :param updates: A dictionary with the desired attributes to update
        :raises: Superdesk.validation.ValidationError: if there are validation errors
        """

        super().validate_patch(original, updates)

        merged = deepcopy(original)
        merged.update(updates)

        # Check that the state hasn't change from a usable/disabled state to draft
        if original.get('state') != SET_STATES.DRAFT:
            if merged.get('state') == SET_STATES.DRAFT:
                raise SamsSetErrors.InvalidStateTransition(original['state'])

        # Check that the destination name hasn't changed for non-draft Sets
        if original.get('state') != SET_STATES.DRAFT:
            if merged.get('destination_name') != original.get('destination_name'):
                raise SamsSetErrors.DestinationChangeNotAllowed()
            elif merged.get('destination_config') != original.get('destination_config'):
                raise SamsSetErrors.DestinationConfigChangeNotAllowed()

        self._validate_destination_name(merged)

    def _validate_destination_name(self, doc):
        """Validates that the desired destination is configured in the system

        :param doc: The provided document to validate
        :raises Superdesk.validation.ValidationError: If there are validation errors
        """

        if not destinations.exists(doc.get('destination_name')):
            raise SamsSetErrors.DestinationNotFound(doc.get('destination_name'))

    def on_delete(self, doc):
        """Validate state on delete

        Sets can only be deleted from the system if they are in the state ``SET_STATES.DRAFT``.

        :param doc: The Set to delete
        :raises: Superdesk.validation.ValidationError: If the Set is not in ``SET_STATES.DRAFT`` state
        """

        if doc.get('state') != SET_STATES.DRAFT:
            raise SamsSetErrors.CannotDeleteActiveSet()

    def get_destination(self, set_id: ObjectId) -> Destination:
        item = self.get_by_id(set_id)

        if not item:
            raise SamsSetErrors.SetNotFound(set_id)

        return destinations.get(item.get('destination_name'))

    def get_provider_instance(self, set_id: ObjectId) -> SamsBaseStorageProvider:
        return self.get_destination(set_id).provider_instance()
