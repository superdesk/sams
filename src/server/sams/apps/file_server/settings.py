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

from sams.default_settings import env, urlparse

HOST = env('SAMS_PUBLIC_HOST', 'localhost')
PORT = int(env('SAMS_PUBLIC_PORT', '5750'))

SERVER_URL = env('SAMS_PUBLIC_URL', 'http://localhost:5750')
server_url = urlparse(SERVER_URL)
SERVER_DOMAIN = server_url.netloc or 'localhost'
API_VERSION = ''
URL_PREFIX = env('SAMS_PUBLIC_URL_PREFIX', server_url.path.lstrip('/')) or ''

RETURN_ERRORS_AS_JSON = False

CORE_APPS = [
    'sams.sets',
    'sams.storage',
    'sams.assets',
]
INSTALLED_APPS = [
    'sams.factory.sentry',
    'sams.api.public'
]

# Specify the type of authentication
SAMS_AUTH_TYPE = env('SAMS_PUBLIC_AUTH_TYPE', 'sams.auth.public')

# Specify api keys for basic auth
CLIENT_API_KEYS = env('SAMS_PUBLIC_API_KEYS', '')

# Specify the location of the log config file
LOG_CONFIG_FILE = env('SAMS_PUBLIC_LOG_CONFIG', 'logging_config.yml')
