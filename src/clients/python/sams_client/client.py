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

from importlib import import_module
import requests
from json import dumps
from typing import Dict, Any, Callable

from .utils import load_config, urlencode
from .endpoints import SamsSetEndpoint, SamsStorageDestinationsEndpoint, SamsAssetEndpoint


class SamsClient(object):
    """Class for Superdesk Asset Managements Service Client

    :var str base_url: The base url for the API
    :var SamsSetEndpoint sets: Access points for the set endpoints

    Usage::

        from sams_client import Client

        configs = {
            'HOST': 'localhost',
            'PORT': '5700',
            'SAMS_AUTH_TYPE': 'sams_client.auth.public',
            'SAMS_AUTH_KEY': ''
        }
        client = SamsClient(configs)
        response = client.request(api='/')
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Constructor for SamsClient class

        :param dict config: Optional config overrides
        """

        if config is None:
            config = {}

        self.config = load_config(config)
        self.setup_auth()
        self.sets: SamsSetEndpoint = SamsSetEndpoint(self)
        self.destinations: SamsStorageDestinationsEndpoint = SamsStorageDestinationsEndpoint(self)
        self.assets: SamsAssetEndpoint = SamsAssetEndpoint(self)

    def request(
        self,
        api: str = '/',
        method: str = 'get',
        headers: Dict[str, Any] = None,
        data: str = None,
        files=None,
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

        if headers is None:
            headers = {}

        if callback is None:
            # set default callback
            callback = self._default_resp_callback
        request = getattr(requests, method.lower())
        base_url = self.config.get('base_url')
        url = f'{base_url}{api}'
        headers = self.auth.apply_headers(headers)
        response = request(url, headers=headers, data=data, files=files)
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
        files=None,
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

        # In case of multipart form data don't send Content-Type
        if 'Content-Type' not in headers and files is None:
            headers['Content-Type'] = 'application/json'

        # In case of multipart form data don't dump
        if not isinstance(data, str) and files is None:
            data = dumps(data)

        return self.request(
            api=url,
            method='post',
            headers=headers,
            data=data,
            files=files,
            callback=callback
        )

    def patch(
        self,
        url: str,
        headers: Dict[str, Any] = None,
        data: str or Dict[str, Any] = None,
        files=None,
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

        # In case of multipart form data don't send Content-Type
        if 'Content-Type' not in headers and files is None:
            headers['Content-Type'] = 'application/json'

        # In case of multipart form data don't dump
        if not isinstance(data, str) and files is None:
            data = dumps(data)

        return self.request(
            api=url,
            method='patch',
            headers=headers,
            data=data,
            files=files,
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

    def setup_auth(self):
        if not self.config['auth_type']:
            raise RuntimeError('Authentication type not specified')

        mod = import_module(self.config['auth_type'])
        if not hasattr(mod, 'get_auth_instance') or not callable(mod.get_auth_instance):
            raise RuntimeError('Configured Authentication type must have a `get_auth_instance` method')

        self.auth = mod.get_auth_instance(
            api_key=self.config['auth_key']
        )
