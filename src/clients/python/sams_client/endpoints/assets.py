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

import json
import requests
from .endpoint import Endpoint
from bson import ObjectId
from typing import Dict, Any, Callable, List, Union, Tuple


class SamsAssetEndpoint(Endpoint):
    """Helper class for the Assets resource

    This class automatically sets ``_read_url`` to ``/consume/assets`` \
    and the ``_write_url`` to ``/produce/assets``
    """

    _read_url = '/consume/assets'
    _read_binary_url = '/consume/assets/binary'
    _write_url = '/produce/assets'
    _read_binary_zip_url = '/consume/assets/compressed_binary'

    def get_by_ids(
        self,
        item_ids: List[ObjectId],
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method to get Assets by ids

        :param list<bson.objectid.ObjectId> item_ids: The Asset IDs
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The Assets, if found
        """

        if not self._read_url:
            return self._return_405()

        return self._client.search(
            url=self._read_url,
            headers=headers,
            callback=callback,
            params={'source': json.dumps({
                'query': {
                    'bool': {
                        'must': [
                            {'terms': {'_id': item_ids}}
                        ]
                    }
                }
            })}
        )

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

    def get_binary_zip_by_id(
        self,
        item_ids: List[Union[ObjectId, str]] = None,
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method to get assets' compressed binaries by its ids

        :param bson.objectid.ObjectId item_ids: The IDs' Array of the asset
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The compressed binaries zip, if found
        """

        item_ids = ','.join(str(item_id) for item_id in item_ids) if item_ids else ''
        if not self._read_binary_zip_url:
            return self._return_405()
        return self._client.get(
            url='{}/{}'.format(
                self._read_binary_zip_url,
                item_ids
            ),
            headers=headers,
            callback=callback
        )

    def get_assets_count(
        self,
        set_ids: [ObjectId] = None,
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> Tuple[Dict[str, int], int]:
        """Helper method to get asset count distribution for given set ids
        will get asset count distribution over all sets if set_ids is None

        :param array bson.objectid.ObjectId set_ids: Id of sets
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: dict<str, int>, int
        """

        if not self._read_url:
            return {}, 405

        # get total asset count distribution over all sets if set_ids is None
        if set_ids is None:
            query = {
                'size': 0,
                'aggs': {'counts': {'terms': {'field': 'set_id'}}}
            }
        # get number of assets for given set_ids
        else:
            query = {
                'query': {'terms': {'set_id': set_ids}},
                'size': 0,
                'aggs': {'counts': {'terms': {'field': 'set_id'}}}
            }

        query = json.dumps(query)
        params = {'source': query}

        response = self._client.get(
            url=self._read_url,
            params=params,
            headers=headers,
            callback=callback
        )
        buckets = response.json().get('_aggregations').get('counts').get('buckets')

        counts = {}
        [counts.update({item.get('key'): item.get('doc_count')}) for item in buckets]
        return counts, response.status_code
