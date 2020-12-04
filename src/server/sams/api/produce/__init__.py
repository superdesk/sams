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
from .assets import ProduceAssetResource, ProduceAssetService, assets_produce_bp
from sams.factory.app import SamsApp
from sams.assets import get_service as get_assets_service
from sams.auth.decorator import blueprint_auth


def init_app(app: SamsApp):
    service = ProduceAssetService(get_assets_service())
    service.app = app
    ProduceAssetResource(
        endpoint_name=ProduceAssetResource.endpoint_name,
        app=app,
        service=service
    )

    @assets_produce_bp.before_request
    @blueprint_auth()
    def before_request():
        """
        Add authentication before request to all blueprint
        """
        pass

    superdesk.blueprint(assets_produce_bp, app)
