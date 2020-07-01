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

from typing import Dict, Any


def get_auth_instance(**kwargs):
    api_key = kwargs['api_key']
    return SamsBasicAuth(api_key)


class SamsBasicAuth(object):
    """Basic Authentication instance
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def apply_headers(self, headers: Dict[str, Any]):
        """Applies Basic Authentication to the request header

        :param dict headers: Dictionary containing request headers
        :rtype: dict
        :return: The headers with Authorization key applied
        """
        headers['Authorization'] = f'Basic {self.api_key}'
        return headers
