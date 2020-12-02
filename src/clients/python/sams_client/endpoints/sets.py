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


class SamsSetEndpoint(Endpoint):
    r"""Helper class for the Sets resource

    This class automatically sets ``_read_url`` to ``/consume/sets`` \
    and the ``_write_url`` to ``/admin/sets``
    """

    _read_url = '/consume/sets'
    _write_url = '/admin/sets'
