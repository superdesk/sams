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

from sams_client.client import SamsClient


class SamsClientAdmin(SamsClient):
    DESTINATIONS_API = '/admin/destinations/'

    def request_destination(self, id):
        return self.request(api=self.DESTINATIONS_API + id)

    def request_destinations(self):
        return self.request(api=self.DESTINATIONS_API)
