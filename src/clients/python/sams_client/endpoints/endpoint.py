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

from bson import ObjectId
from typing import Dict, List, Any, Callable
import requests


class Endpoint:
    r"""Base helper class for endpoint specifics

    :var sams_client.client.SamsClient _client: Reference to the parent client instance
    :var str _read_url: The URL for all read based requests
    :var str _write_url: The URL for all write based requests

    By using this endpoint, you can implement specific logic required for each type of resource \
    so that you can intercept read/write requests to maniupulate or sanatize the request.

    Usage::

        # Add a new file under sams_client.endpoints for the resource
        # i.e. sams_client.endpoints.sets.py
        from .endpoint import Endpoint


        class SamsSetEndpoint(Endpoint):
            _read_url = '/consume/sets'
            _write_url = '/admin/sets'

    Then add a new member variable to :class:`sams_client.client.SamsClient`
    for users to utilise this new endpoint
    """

    _read_url: str
    _write_url: str

    def __init__(self, client):
        # Placing this import at the top of the file causes a cyclic import
        # so placing it here to have strong type / autocomplete
        from sams_client import SamsClient

        self._client: SamsClient = client

    def _return_405(self) -> requests.Response:
        """Helper method to construct a 405 response

        :rtype: requests.Response
        :return: Response with status_code=405
        """

        response = requests.Response()
        response.status_code = 405
        return response

    def search(
        self,
        params: Dict[str, Any] = None,
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method to search this endpoint

        :param dict params: Dictionary containing the search arguments
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The search response
        """

        if not self._read_url:
            return self._return_405()

        return self._client.search(
            url=self._read_url,
            params=params,
            headers=headers,
            callback=callback
        )

    def get_by_id(
        self,
        item_id: ObjectId,
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method to get a document by its id

        :param bson.objectid.ObjectId item_id: The ID of the document
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The document, if found
        """

        if not self._read_url:
            return self._return_405()

        return self._client.get(
            url='{}/{}'.format(
                self._read_url,
                str(item_id)
            ),
            headers=headers,
            callback=callback
        )

    def create(
        self,
        docs: List[Dict[str, Any]],
        headers: Dict[str, Any] = None,
        files=None,
        external_user_id: str = None,
        external_session_id: str = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method to create a new document(s)

        :param list[dict] docs: The list of documents to create
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The newly created document
        """

        if not self._write_url:
            return self._return_405()

        return self._client.post(
            url=self._write_url,
            headers=headers,
            data=docs,
            files=files,
            external_user_id=external_user_id,
            external_session_id=external_session_id,
            callback=callback
        )

    def update(
        self,
        item_id: ObjectId,
        updates: Dict[str, Any],
        headers: Dict[str, Any] = None,
        files=None,
        external_user_id: str = None,
        external_session_id: str = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method to update an existing document

        :param bson.objectid.ObjectId item_id: The ID of the existing document
        :param dict updates: Dictionary with the updates to apply
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The updated document
        """
        if not self._write_url:
            return self._return_405()

        return self._client.patch(
            url='{}/{}'.format(
                self._write_url,
                str(item_id)
            ),
            headers=headers,
            data=updates,
            files=files,
            external_user_id=external_user_id,
            callback=callback
        )

    def delete(
        self,
        item_id: ObjectId,
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method to delete an existing document

        :param bson.objectid.ObjectId item_id: The ID of the existing document
        :param dict headers: Dictionary of the headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The delete response
        """

        if not self._write_url:
            return self._return_405()

        return self._client.delete(
            url='{}/{}'.format(
                self._write_url,
                str(item_id)
            ),
            headers=headers,
            callback=callback
        )
