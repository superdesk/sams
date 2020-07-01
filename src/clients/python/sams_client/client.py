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

from .utils import load_config
from importlib import import_module
import requests


class SamsClient(object):
    """Class for Superdesk Asset Managements Service Client

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

    def __init__(self, config={}):
        """Constructor for SamsClient class
        """
        self.config = load_config(config)
        self.setup_auth()

    def request(self, api='/', method='get',
                headers={}, data=None, callback=None):
        """Handle request methods
        """
        if callback is None:
            # set default callback
            callback = self._default_resp_callback
        request = getattr(requests, method.lower())
        base_url = self.config.get('base_url')
        url = f'{base_url}{api}'
        headers = self.auth.apply_headers(headers)
        response = request(url, headers=headers, data=data)
        return callback(response)

    def _default_resp_callback(self, response):
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
