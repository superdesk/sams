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

from superdesk.default_settings import strtobool, env, urlparse

HOST = env('SAMS_HOST', '0.0.0.0')
PORT = int(env('SAMS_PORT', '5700'))

SERVER_URL = env('SAMS_URL', 'http://localhost:5700')
server_url = urlparse(SERVER_URL)
SERVER_DOMAIN = server_url.netloc or 'localhost'
URL_PREFIX = env('URL_PREFIX', server_url.path.lstrip('/')) or ''

#: mongo db name, only used when mongo_uri is not set
MONGO_DBNAME = env('MONGO_DBNAME', 'sams')

#: full mongodb connection uri, overrides ``MONGO_DBNAME`` if set
MONGO_URI = env('MONGO_URI', 'mongodb://localhost/%s' % MONGO_DBNAME)

#: allow all mongo queries
MONGO_QUERY_BLACKLIST = []

#: elastic url
ELASTICSEARCH_URL = env('ELASTICSEARCH_URL', 'http://localhost:9200')

#: elastic index name
ELASTICSEARCH_INDEX = env('ELASTICSEARCH_INDEX', 'sams')

if env('ELASTIC_PORT'):
    ELASTICSEARCH_URL = env('ELASTIC_PORT').replace('tcp:', 'http:')

ELASTICSEARCH_BACKUPS_PATH = env('ELASTICSEARCH_BACKUPS_PATH', '')

# Eve config attributes
IF_MATCH = True
BANDWIDTH_SAVER = False
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S+0000'
ELASTIC_DATE_FORMAT = '%Y-%m-%d'
ELASTIC_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
PAGINATION_LIMIT = 200
MERGE_NESTED_DOCUMENTS = True
RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length', '_id']
RETURN_MEDIA_AS_BASE64_STRING = False
VERSION = '_current_version'

#: uses for generation of media url ``(<media_prefix>/<media_id>)``::
MEDIA_PREFIX = env('MEDIA_PREFIX', '%s/upload-raw' % SERVER_URL.rstrip('/'))
MEDIA_PREFIXES_TO_FIX = None
JSON_SORT_KEYS = False
VALIDATION_ERROR_STATUS = 400
VALIDATION_ERROR_AS_LIST = True

CACHE_CONTROL = 'max-age=0, no-cache'

X_DOMAINS = '*'
X_MAX_AGE = 24 * 3600
X_HEADERS = ['Content-Type', 'Authorization', 'If-Match']

#: Specify what modules should be enabled
CORE_APPS = [
    'sams.sets'
]
INSTALLED_APPS = [
    'sams.factory.sentry'
]

# Specify the type of authentication
SAMS_AUTH_TYPE = 'sams.auth.public'

# Specify the location of the log config file
LOG_CONFIG_FILE = 'logging_config.yml'

#: Sentry DSN - will report exceptions there
SENTRY_DSN = env('SENTRY_DSN')
SENTRY_INCLUDE_PATHS = ['sams']

# Flask/Application variables
FLASK_ENV = env('FLASK_ENV', 'development')
DEBUG = strtobool(env('SAMS_DEBUG', 'true'))
SAMS_TESTING = strtobool(env('SAMS_TESTING', 'true'))

# Fix bug in Superdesk-Core/notification not using .get
CELERY_BROKER_URL = None
