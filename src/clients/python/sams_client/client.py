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
from json import dumps
from typing import Dict, Any, Callable

from .utils import get_base_url, urlencode
from .endpoints import SamsSetEndpoint


class SamsClient(object):
    """Class for Superdesk Asset Managements Service Client

    :var str base_url: The base url for the API
    :var SamsSetEndpoint sets: Access points for the set endpoints

    Usage::

        from sams_client import Client

        configs = {
            'HOST': 'localhost',
            'PORT': '5700'
        }
        client = SamsClient(configs)
        response = client.request(api='/')
    """

    def __init__(self, configs: Dict[str, Any] = None):
        """Constructor for SamsClient class

        :param dict configs: Optional config overrides
        """

        if configs is None:
            configs = {}

        self.base_url: str = get_base_url(configs)
        self.sets: SamsSetEndpoint = SamsSetEndpoint(self)

    def request(
        self,
        api: str = '/',
        method: str = 'get',
        headers: Dict[str, Any] = None,
        data: str = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Handle request methods

        :param str api: The url for the request
        :param str method: The HTTP method to use
        :param dict headers: Dictionary of headers to apply
        :param data: The body for the request
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The API response
        """

        if callback is None:
            # set default callback
            callback = self._default_resp_callback
        request = getattr(requests, method.lower())
        url = f'{self.base_url}{api}'
        response = request(url, headers=headers, data=data)
        return callback(response)

    def get(
        self,
        url: str,
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method for GET requests

        :param str url: The url to get
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The API response
        """

        return self.request(
            api=url,
            method='get',
            headers=headers,
            callback=callback
        )

    def search(
        self,
        url: str,
        args: Dict[str, Any] = None,
        headers: Dict[str, any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method for GET requests with query args

        Uses :mod:`sams_client.utils.urlencode` to convert args to a query string.

        :param str url: The url to get
        :param dict args: Dictionary of query args to apply
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The API response
        """

        return self.get(
            url=urlencode(url, args),
            headers=headers,
            callback=callback
        )

    def post(
        self,
        url: str,
        headers: Dict[str, Any] = None,
        data: str or Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method for POST requests

        Converts the ``data`` to a string using :mod:`json.dumps` if ``data`` is not a string.

        :param str url: The url to post to
        :param dict headers: Dictionary of headers to apply
        :param data: The body for the request
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The API response
        """

        if headers is None:
            headers = {}

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        if not isinstance(data, str):
            data = dumps(data)

        return self.request(
            api=url,
            method='post',
            headers=headers,
            data=data,
            callback=callback
        )

    def patch(
        self,
        url: str,
        headers: Dict[str, Any] = None,
        data: str or Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method for PATCH requests

        Converts the ``data`` to a string using :mod:`json.dumps` if ``data`` is not a string.

        :param str url: The url to patch to
        :param dict headers: Dictionary of headers to apply
        :param data: The body of the request
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The API response
        """

        if headers is None:
            headers = {}

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        return self.request(
            api=url,
            method='patch',
            headers=headers,
            data=dumps(data) if not isinstance(data, str) else data,
            callback=callback
        )

    def delete(
        self,
        url: str,
        headers: Dict[str, Any] = None,
        callback: Callable[[requests.Response], requests.Response] = None
    ) -> requests.Response:
        """Helper method for DELETE requests

        :param str url: The url to delete
        :param dict headers: Dictionary of headers to apply
        :param callback: A callback function to manipulate the response
        :rtype: requests.Response
        :return: The API response
        """

        return self.request(
            api=url,
            method='delete',
            headers=headers,
            callback=callback
        )

    def _default_resp_callback(self, response: requests.Response) -> requests.Response:
        """Default response callback

        :param requests.Response response: The original response object
        :rtype: requests.Response
        :return: The original API response without any changes
        """

        return response
