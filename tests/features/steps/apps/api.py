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

from typing import Dict, Any

from sams.default_settings import INSTALLED_APPS
from sams.storage.destinations import destinations
from sams.storage.providers.amazon import AmazonS3Provider
from sams.apps.api.app import get_app

from sams_client import SamsClient
from sams_client.errors import SamsAmazonS3Errors

from .base import BaseTestApp


class TestAPI(BaseTestApp):

    def get_config(self) -> Dict[str, Any]:
        return {
            'INSTALLED_APPS': INSTALLED_APPS
        }

    def get_app(self, config: Dict[str, Any]):
        return get_app('sams_api', config=config)

    def wait_startup(self):
        super().wait_startup()
        self.create_s3_buckets()

    def create_s3_buckets(self):
        for destination in destinations.all().values():
            if destination.provider.type_name != AmazonS3Provider.type_name:
                continue

            try:
                destination.provider_instance().create_bucket()
            except SamsAmazonS3Errors.BucketAlreadyExists:
                continue


def get_api(context) -> TestAPI:
    try:
        app = getattr(context, 'app_api')
    except AttributeError:
        app = TestAPI()
        app.init()
        context.app_api = app

    return app


def get_api_client(context) -> SamsClient:
    return get_api(context).client
