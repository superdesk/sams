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
    return SamsPublicAuth()


class SamsPublicAuth(object):
    """Public Authentication instance
    """

    def __init__(self):
        pass

    def apply_headers(self, headers: Dict[str, Any]):
        """Returns the request header

        :param headers: Dictionary containing request headers
        :rtype: dict
        :return: Return back the headers
        """
        return headers
