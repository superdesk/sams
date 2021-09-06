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

from .client import SamsClient # noqa
from .schemas.assets import IAsset, IAssetTag, IAssetRendition, IAssetRenditionArgs # noqa

__version__ = '0.3.0'
__all__ = ('SamsClient', 'IAsset', 'IAssetTag', 'IAssetRendition', 'IAssetRenditionArgs')
