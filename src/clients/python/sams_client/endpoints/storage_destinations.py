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

from .endpoint import Endpoint


class SamsStorageDestinationsEndpoint(Endpoint):
    r"""Helper class for the StorageDestinatino resource

    This class automatically sets ``_read_url`` to ``/admin/destinations`` \
    and leaves the ``_write_url`` as ``None``
    """

    _read_url = '/admin/destinations'
    _write_url = None
