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

"""

A set a collection of *Assets*. It is used as a way to organise and restrict access to
the *Assets* it holds.

All access to the binary or metadata of assets will go through this service. There must
be at least one Set configured in the system.

A single Set can be designated as the default Set. When access is requested to an asset
without a set being provided, the default set will be used.

Usage
-----
The Set service instance can be found under :data:`sams.sets.service` and used all::

    from sams_client import SamsClient, IAsset, IAssetTag

    client = SamsClient()

    # Load the image file
    with open("example_image.png", "rb") as image_file:
        asset_binary = image_file.read()

    set_id = client.sets.search().json()["_items"][0]["_id"]

    # Upload a new Image Asset
    response = client.assets.create(
        docs=IAsset(
            set_id=set_id,
            filename="example_image.png",
            name="test image renditions",
            description="example image to test renditions",
            tags=[
                IAssetTag(code="test", name="test"),
                IAssetTag(code="rendition", name="rendition")
            ]
        ),
        files={"binary": asset_binary},
        external_user_id="test_user_id"
    )
    new_asset = response.json()

    # Generate a rendition
    client.images.generate_rendition(
        new_asset["_id"],
        width=640,
        height=640,
        keep_proportions=True
    )

    # Download the newly created rendition
    image_rendition = client.images.download(
        new_asset["_id"],
        width=640,
        height=640,
        keep_proportions=True
    )
"""

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
    ) -> requests.Response:
        r"""Download an Image, optionally providing image dimensions

        :param str item_id: The Asset ID
        :param int width: Desired image width (optional)
        :param int height: Desired image height (optional)
        :param bool keep_proportions: If `true`, keeps image width/height ratio
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The Asset binary, optionally resized
        """

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
    ) -> requests.Response:
        r"""Generates an Image rendition

        :param str item_id: The Asset ID
        :param int width: Desired image width (optional)
        :param int height: Desired image height (optional)
        :param bool keep_proportions: If `true`, keeps image width/height ratio
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: 200 status code if rendition generated successfully
        """

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
