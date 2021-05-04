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

from typing import Dict, Any, List
from copy import deepcopy
from bson import ObjectId

from flask import current_app as app

from sams_client.schemas import SET_STATES

from sams.factory.service import SamsService
from sams.storage.destinations import Destination, destinations
from sams.storage.providers.base import SamsBaseStorageProvider
from sams_client.errors import SamsSetErrors
from sams.utils import get_external_user_id

from superdesk.services import Service
from superdesk.utc import utcnow


class SetsService(SamsService):
    def post(self, docs: List[Dict[str, Any]], **kwargs) -> List[ObjectId]:
        """Stores the metadata

        :param docs: An array of metadata to create
        :param kwargs: Dictionary containing the keyword arguments
        :return: list of generated IDs for the new documents
        :rtype: list[bson.objectid.ObjectId]
        """
        for doc in docs:
            doc['firstcreated'] = utcnow()
            doc['versioncreated'] = utcnow()
            external_user_id = get_external_user_id()

            if external_user_id:
                doc['original_creator'] = external_user_id
                doc['version_creator'] = external_user_id

            self.validate_post(doc)

        return super(Service, self).post(docs, **kwargs)

    def patch(self, item_id: ObjectId, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Updates the metadata


        :param bson.objectid.ObjectId item_id: ID for the Set
        :param dict updates: Dictionary containing the desired metadata to update
        :return: Dictionary containing the updated attributes of the Set
        :rtype: dict
        """
        original = self.get_by_id(item_id)
        self.validate_patch(original, updates)

        updates['versioncreated'] = utcnow()
        external_user_id = get_external_user_id()

        if external_user_id:
            updates['version_creator'] = external_user_id

        return super(Service, self).patch(item_id, updates)

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
        r"""Validates the Set on update

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
        count = self.get_asset_count(doc.get('_id'))
        if doc.get('state') == SET_STATES.USABLE or (doc.get('state') == SET_STATES.DISABLED and count):
            raise SamsSetErrors.CannotDeleteActiveSet()

    def get_destination(self, set_id: ObjectId) -> Destination:
        item = self.get_by_id(set_id)

        if not item:
            raise SamsSetErrors.SetNotFound(set_id)

        return destinations.get(item.get('destination_name'))

    def get_provider_instance(self, set_id: ObjectId) -> SamsBaseStorageProvider:
        return self.get_destination(set_id).provider_instance()

    def get_asset_count(self, set_id: ObjectId):
        from sams.assets import get_service as get_assets_service
        service = get_assets_service()
        response = service.get(req=None, lookup={'set_id': set_id})
        return response.count()

    def get_max_asset_size(self, set_id: ObjectId) -> int:
        """Returns the maximum allowed size of an Asset for a Set

        Based on the configured settings, this method returns:
            * ``Set.maximum_asset_size`` if ``MAX_ASSET_SIZE == 0``
            * ``MAX_ASSET_SIZE`` if ``Set.maximum_asset_size == 0``
            * Otherwise whichever is lowest

        :param bson.objectid.ObjectId set_id: The ID of the Set
        :return: The configured MAX_ASSET_SIZE of Set.maximum_asset_size, whichever is lower
        :rtype: int
        """

        set_item = self.get_by_id(set_id)
        max_set_size = set_item.get('maximum_asset_size') or 0
        max_app_size = app.config.get('MAX_ASSET_SIZE') or 0

        if max_app_size == 0:
            return max_set_size
        elif max_set_size == 0:
            return max_app_size
        else:
            return max_set_size if max_set_size < max_app_size else max_app_size
