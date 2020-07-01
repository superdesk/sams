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

from eve.auth import BasicAuth
from sams.logging import logger
from flask import abort, request


def get_auth_instance(**kwargs):
    api_keys = kwargs['api_keys']
    return SamsBasicAuth(api_keys)


class SamsBasicAuth(BasicAuth):
    """Basic Auth instance
    """

    def __init__(self, api_keys=None):
        api_keys = list(
            filter(lambda key: key != '', api_keys or [])
        )

        if len(api_keys) == 0:
            abort(501, 'No API Keys provided')

        self.api_keys = api_keys

    def authorized(self, allowed_roles, resource, method=None):
        auth_token = request.headers.get('Authorization')
        return auth_token and self.check_auth(auth_token, allowed_roles, resource, method)

    def authenticate(self):
        """Returns a standard 401
        """
        abort(401, description='Please provide proper credentials')

    def check_auth(self, auth_token, allowed_roles, resource, method):
        """This function is called to check if the API key in request header
        exists in the api_keys in app config

        :param auth_token: API key in request header
        :param allowed_roles: allowed user roles
        :param resource: resource being requested
        :param method: HTTP method being executed (POST, GET, etc.)
        """
        return auth_token.lstrip('Basic ') in self.api_keys
