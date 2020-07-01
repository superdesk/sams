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

from eve.utils import config

from superdesk.services import Service
from superdesk.validation import ValidationError


class SamsService(Service):
    """Sams Service

    Base service for all endpoints, defines the basic implementation for CRUD functionality.
    This version differs from Superdesk.services.Service to provide validation on internal usage
    """

    def get_by_id(self, id, field=config.ID_FIELD):
        """Helper function to retrieve a document by id

        :param bson.objectid.ObjectId id: ID for the document
        :param field: field to use when searching for the document (defaults to '_id')
        :return: document found in the system
        """

        kwargs = {field: id}
        return self.find_one(req=None, **kwargs)

    def post(self, docs, **kwargs):
        """Create new documents for the specific resource

        :param docs: An array of documents to create
        :param kwargs: dictionary containing the keyword arguments
        :return: list of generated IDs for the new documents
        """

        for doc in docs:
            self.validate_post(doc)
        return super().post(docs, **kwargs)

    def patch(self, id, updates):
        """Update an existing document for the specific resource

        :param bson.ObjectId id: ID for the document
        :param updates: Dictionary containing the desired attributes to update
        :return: dictionary containing the updated attributes of the document
        """

        original = self.get_by_id(id)
        self.validate_patch(original, updates)
        return super().patch(id, updates)

    def validate_post(self, doc):
        """Validates the document upon creation

        The validation performed in this step is provided by Eve/Cerberus using the defined
        schema for the resource.

        :param doc: The provided document to validate
        :raises Superdesk.validation.ValidationError: If there are validation errors
        """

        validator = self._validator()
        if not validator:
            return

        validator.validate(doc)
        if validator.errors:
            raise ValidationError(validator.errors)

    def validate_patch(self, original, updates):
        """Validates the document upon update

        The validation performed in this step is provided by Eve/Cerberus using the defined
        schema for the resource.

        :param original: The original document from the database
        :param updates: A dictionary with the desired attributes to update
        :raises Superdesk.validation.ValidationError: If there are validation errors
        """

        validator = self._validator()
        if not validator:
            return

        validator.validate_update(updates, original.get(config.ID_FIELD), original)
        if validator.errors:
            raise ValidationError(validator.errors)
