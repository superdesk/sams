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

from typing import Dict, Any, Callable, Union, Optional

from bson import ObjectId
import requests


class SamsImagesEndpoint:
    """Helper class for Image Assets"""

    _download_image_url = '/consume/assets/images'
    _generate_image_rendition_url = '/produce/assets/images'

    def __init__(self, client):
        # Placing this import at the top of the file causes a cyclic import
        # so placing it here to have strong type / autocomplete
        from sams_client import SamsClient

        self._client: SamsClient = client

    def download(
        self,
        item_id: Union[ObjectId, str],
        width: Optional[int] = None,
        height: Optional[int] = None,
        keep_proportions: Optional[bool] = True,
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ):
        params = {}

        if width:
            params['width'] = width

        if height:
            params['height'] = height

        if keep_proportions:
            params['keep_proportions'] = keep_proportions

        return self._client.get(
            url=f'{self._download_image_url}/{item_id}',
            params=params,
            headers=headers,
            callback=callback
        )

    def generate_rendition(
            self,
            item_id: Union[ObjectId, str],
            width: Optional[int] = None,
            height: Optional[int] = None,
            keep_proportions: Optional[bool] = True,
            headers: Dict[str, Any] = None,
            callback: Callable[[requests.Response], requests.Response] = None
    ):
        params = {}

        if width:
            params['width'] = width

        if height:
            params['height'] = height

        if keep_proportions:
            params['keep_proportions'] = keep_proportions

        return self._client.post(
            url=f'{self._generate_image_rendition_url}/{item_id}',
            params=params,
            headers=headers,
            callback=callback
        )
