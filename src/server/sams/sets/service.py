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
from superdesk.validation import ValidationError

from sams.factory.service import SamsService
from .resource import SET_STATES


class SetsService(SamsService):
    def validate_patch(self, original, updates):
        """Validates the Set on update

        The following additional validation is performed on Sets being updated:
            * Once a set has changed from 'draft' state, it can never return to 'draft'
            * Once a set has changed from 'draft' state, 'destination_name' cannot be changed

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
                raise ValidationError({
                    'state': 'Cannot change state from "{}" to draft'.format(original['state'])
                })

        # Check that the destination name hasn't changed for non-draft Sets
        if merged.get('state') != SET_STATES.DRAFT:
            if merged.get('destination_name') != original.get('destination_name'):
                raise ValidationError({
                    'destination_name': 'Destination can only be changed in draft state'
                })

    def on_delete(self, doc):
        """Validate state on delete

        Sets can only be deleted from the system if they are in the state ``SET_STATES.DRAFT``.

        :param doc: The Set to delete
        :raises: Superdesk.validation.ValidationError: If the Set is not in ``SET_STATES.DRAFT`` state
        """

        if doc.get('state') != SET_STATES.DRAFT:
            raise ValidationError({
                'delete': 'Can only delete Sets that are in draft state'
            })
