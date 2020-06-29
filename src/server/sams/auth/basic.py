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


def get_auth_instance(api_keys):
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
        """Returns a standard a 401
        """
        abort(401, description='Please provide proper credentials')

    def check_auth(self, auth_token, allowed_roles, resource, method):
        return auth_token.lstrip('Basic ') in self.api_keys
