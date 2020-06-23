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
from .utils import get_base_url


class SamsClient(object):
    """Class for Superdesk Asset Managements Service Client

    Usage::

        from sams_client import Client

        configs = {
            'HOST': 'localhost',
            'PORT': '5700'
        }
        client = SamsClient(configs)
        response = client.request(api='/')
    """

    def __init__(self, configs={}):
        """Constructor for SamsClient class
        """
        self.base_url = get_base_url(configs)

    def request(self, api='/', method='get',
                headers=None, data=None, callback=None):
        """Handle request methods
        """
        if callback is None:
            # set default callback
            callback = self._default_resp_callback
        request = getattr(requests, method.lower())
        url = f'{self.base_url}{api}'
        response = request(url, headers=headers, data=data)
        response.raise_for_status()
        return callback(response)

    def _default_resp_callback(self, response):
        return response
