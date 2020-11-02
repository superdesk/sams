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

from os import path, devnull
import sys
from threading import Thread
from time import sleep
from copy import deepcopy

from sams.factory.app import SamsApp

from sams_client import SamsClient

from tests.server.conftest import get_test_config


class BaseTestApp:
    def __init__(self):
        self.app: SamsApp = None
        self.client: SamsClient = None
        self._sys_client: SamsClient = None
        self.thread: Thread = None

    def get_config(self) -> Dict[str, Any]:
        raise NotImplementedError()

    def get_app(self, config: Dict[str, Any]):
        raise NotImplementedError()

    def init(self, config_overrides=None):
        if config_overrides is None:
            config_overrides = {}

        self.stop()

        config = deepcopy(get_test_config())
        config.update(self.get_config())
        # config = deepcopy(self.get_config())
        config['INSTALLED_APPS'] += ['tests.fixtures.prepopulate']
        config.update({
            'DEBUG': False,
            'TESTING': False,
            'LOG_CONFIG_FILE': path.join(
                path.dirname(path.abspath(__file__)),
                'logging_config.yml'
            ),
        })
        config.update(config_overrides)
        self.app = self.get_app(config=config)
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
            debug=True,
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
                    print('Too many attempt while waiting for SAMS File Server to shutdown')
                    assert False, 'Failed to shutdown the SAMS File Server application'
                self._sys_client.request()
                sleep(0.5)
                attempts += 1
            except Exception:
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
                    print('Too many attempts while waiting for SAMS File Server to start')
                    assert False, 'Failed to start the SAMS File Server application'
                elif self._sys_client.request().status_code == 200:
                    break
                else:
                    attempts += 1
                    sleep(0.5)
            except Exception:
                attempts += 1
                sleep(0.5)
