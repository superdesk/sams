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
    return MockAuthReject()


class MockAuthReject(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return False

    def authorized(self, allowed_roles, resource, method):
        return False
