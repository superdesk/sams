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

import requests
from .endpoint import Endpoint
from bson import ObjectId
from typing import Dict, Any, Callable


class SamsAssetEndpoint(Endpoint):
    """Helper class for the Assets resource

    This class automatically sets ``_read_url`` to ``/consume/assets`` \
    and the ``_write_url`` to ``/produce/assets``
    """

    _read_url = '/consume/assets'
    _read_binary_url = '/consume/assets/binary'
    _write_url = '/produce/assets'

    def get_binary_by_id(
        self,
        item_id: ObjectId,
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method to get an asset binary by its id

        :param bson.objectid.ObjectId item_id: The ID of the asset
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The binary, if found
        """

        if not self._read_binary_url:
            return self._return_405()

        return self._client.get(
            url='{}/{}'.format(
                self._read_binary_url,
                str(item_id)
            ),
            headers=headers,
            callback=callback
        )
