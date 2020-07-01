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


def get_auth_instance(**kwargs):
    return PublicAuth()


class PublicAuth(BasicAuth):
    """Allow all access to public - No authentication required

    To use this method, set ``SAMS_AUTH_TYPE`` to ``'sams.auth.public'`` in your settings.py
    """

    def check_auth(self, username, password, allowed_roles, resource, method):
        """"""

        return True

    def authorized(self, allowed_roles, resource, method):
        """"""

        return True
