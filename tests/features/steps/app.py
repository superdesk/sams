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

from os import environ, path, devnull
import sys
from threading import Thread
from time import sleep
from copy import deepcopy

from requests.exceptions import ConnectionError

from sams.factory.app import SamsApp
from sams.default_settings import INSTALLED_APPS
from sams.storage.destinations import destinations
from sams.storage.providers.amazon import AmazonS3Provider

from sams_client import SamsClient
from sams_client.errors import SamsAmazonS3Errors

from tests.server.conftest import get_test_config as get_test_config_base


class TestApp:
    def __init__(self):
        self.app: SamsApp = None
        self.client: SamsClient = None
        self._sys_client: SamsClient = None
        self.thread: Thread = None

    def init(self, config_overrides=None):
        if config_overrides is None:
            config_overrides = {}

        self.stop()

        config = deepcopy(get_test_config())
        config.update(config_overrides)
        self.app = SamsApp('sams', config=config)
        self.client = self.create_client_instance()
        self._sys_client = self.create_client_instance(override_auth=True)

    def create_client_instance(self, config_overrides=None, override_auth=False):
        host, port = self.get_host_port()
        config = {
            'HOST': host,
            'PORT': port
        }

        if override_auth and\
                self.app.config.get('SAMS_AUTH_TYPE') == 'sams.auth.basic' and\
                self.app.config.get('CLIENT_API_KEYS'):
            config.update({
                'SAMS_AUTH_TYPE': 'sams_client.auth.basic',
                'SAMS_AUTH_KEY': self.app.config['CLIENT_API_KEYS'].split(',')[0]
            })

        if config_overrides:
            config.update(config_overrides)

        return SamsClient(config)

    def get_host_port(self):
        host_port = self.app.config['SERVER_NAME'].split(':')
        return host_port[0], host_port[1]

    def start(self):
        self.stop()

        self.thread = Thread(target=self.run)

        # Temporarily redirect stdout to /dev/null
        # So Flask doesn't dump startup log
        stdout = sys.stdout
        sys.stdout = open(devnull, 'w')
        self.thread.start()
        self.wait_startup()

        # Restore original stdout functionality
        sys.stdout = stdout

    def run(self):
        host, port = self.get_host_port()
        self.app.run(
            host=host,
            port=port,
            debug=False,
            use_reloader=False
        )

    def stop(self):
        if self.thread:
            self.prepopulate([{'method': 'shutdown'}])
            self.wait_shutdown()

    def prepopulate(self, data):
        self._sys_client.post(
            url='/tests/prepopulate',
            data=data
        )

    def wait_shutdown(self):
        attempts = 0
        while True:
            try:
                if attempts >= 5:
                    print('Too many attempt while waiting for SAMS to shutdown')
                    assert False, 'Failed to shutdown the SAMS application'
                self._sys_client.request()
                sleep(0.5)
                attempts += 1
            except ConnectionError:
                break

        self.app = None
        self.client = None
        self._sys_client = None
        self.thread = None

    def wait_startup(self):
        attempts = 0
        while True:
            try:
                if attempts >= 5:
                    print('Too many attempts while waiting for SAMS to start')
                    assert False, 'Failed to start the SAMS application'
                elif self._sys_client.request().status_code == 200:
                    break
            except ConnectionError:
                attempts += 1
                sleep(0.5)

        self.create_s3_buckets()

    def create_s3_buckets(self):
        for destination in destinations.all().values():
            if destination.provider.type_name != AmazonS3Provider.type_name:
                continue

            try:
                destination.provider_instance().create_bucket()
            except SamsAmazonS3Errors.BucketAlreadyExists:
                continue


def get_test_config():
    INSTALLED_APPS.append('tests.fixtures.prepopulate')
    config = get_test_config_base()
    config.update({
        'DEBUG': False,
        'TESTING': False,
        'LOG_CONFIG_FILE': path.join(
            path.dirname(path.abspath(__file__)),
            'logging_config.yml'
        ),
        'INSTALLED_APPS': INSTALLED_APPS
    })

    return config


def get_app(context) -> TestApp:
    try:
        app = getattr(context, 'app')
    except AttributeError:
        app = TestApp()
        app.init()
        context.app = app

    return app


def get_client(context) -> SamsClient:
    return get_app(context).client
