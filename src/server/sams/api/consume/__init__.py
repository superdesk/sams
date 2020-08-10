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

import superdesk
from .sets import ConsumeSetResource, ConsumeSetService
from .assets import ConsumeAssetResource, ConsumeAssetService, assets_bp
from sams.factory.app import SamsApp
from sams.sets import get_service as get_set_service
from sams.assets import get_service as get_asset_service
from sams.auth.decorator import blueprint_auth


def init_app(app: SamsApp):
    ConsumeSetResource(
        endpoint_name=ConsumeSetResource.endpoint_name,
        app=app,
        service=ConsumeSetService(get_set_service())
    )

    ConsumeAssetResource(
        endpoint_name=ConsumeAssetResource.endpoint_name,
        app=app,
        service=ConsumeAssetService(get_asset_service())
    )

    @assets_bp.before_request
    @blueprint_auth()
    def before_request():
        """
        Add authentication before request to all blueprint
        """
        pass

    superdesk.blueprint(assets_bp, app)
