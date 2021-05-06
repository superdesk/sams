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

HOST = env('SAMS_HOST', 'localhost')
PORT = int(env('SAMS_PORT', '5700'))

SERVER_URL = env('SAMS_URL', 'http://localhost:5700')
server_url = urlparse(SERVER_URL)
SERVER_DOMAIN = server_url.netloc or 'localhost'
API_VERSION = ''
URL_PREFIX = env('SAMS_URL_PREFIX', server_url.path.lstrip('/')) or ''

SAMS_PUBLIC_URL = env('SAMS_PUBLIC_URL')

#: mongo db name, only used when mongo_uri is not set
MONGO_DBNAME = env('SAMS_MONGO_DBNAME', 'sams')

#: full mongodb connection uri, overrides ``MONGO_DBNAME`` if set
MONGO_URI = env('SAMS_MONGO_URI', 'mongodb://localhost/%s' % MONGO_DBNAME)

#: allow all mongo queries
MONGO_QUERY_BLACKLIST = []

#: elastic url
ELASTICSEARCH_URL = env('SAMS_ELASTICSEARCH_URL', 'http://localhost:9200')

#: elastic index name
ELASTICSEARCH_INDEX = env('SAMS_ELASTICSEARCH_INDEX', 'sams')

if env('SAMS_ELASTIC_PORT'):
    ELASTICSEARCH_URL = env('SAMS_ELASTIC_PORT').replace('tcp:', 'http:')

ELASTICSEARCH_BACKUPS_PATH = env('SAMS_ELASTICSEARCH_BACKUPS_PATH', '')

ELASTICSEARCH_SETTINGS = {
    'settings': {
        'analysis': {
            'tokenizer': {
                # Tokenizer for characters that *may* be used
                # in filenames
                'filename_tokenizer': {
                    'type': 'char_group',
                    'tokenize_on_chars': [
                        'whitespace',
                        '-',
                        '_',
                        '.',
                        '!',
                        '?',
                        ','
                    ]
                }
            },
            'analyzer': {
                # Analyzer for fields that contain file-like names
                'filename_analyzer': {
                    'type': 'custom',
                    'filter': [
                        'lowercase',
                        'asciifolding'
                    ],
                    'tokenizer': 'filename_tokenizer'
                }
            }
        }
    }
}

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

RETURN_ERRORS_AS_JSON = True

#: uses for generation of media url ``(<media_prefix>/<media_id>)``::
MEDIA_PREFIX = env('SAMS_MEDIA_PREFIX', '%s/upload-raw' % SERVER_URL.rstrip('/'))
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
    'sams.sets',
    'sams.storage',
    'sams.assets',
    'sams.commands',
]
INSTALLED_APPS = [
    'sams.factory.sentry',
    'sams.api.admin',
    'sams.api.consume',
    'sams.api.produce'
]

STORAGE_PROVIDERS = [
    'sams.storage.providers.mongo.MongoGridFSProvider',
    'sams.storage.providers.amazon.AmazonS3Provider',
]

# Uncomment this next line and modify the config to add MongoGridFS storage destination
# STORAGE_DESTINATION_1 = 'MongoGridFS,Default,mongodb://sams/sams'

# Specify the type of authentication
SAMS_AUTH_TYPE = env('SAMS_AUTH_TYPE', 'sams.auth.public')

# Specify api keys for basic auth
CLIENT_API_KEYS = env('SAMS_CLIENT_API_KEYS', '')

# Specify the maximum size of an Asset
MAX_ASSET_SIZE = int(env('SAMS_MAX_ASSET_SIZE', '0'))

# Specify the location of the log config file
LOG_CONFIG_FILE = env('SAMS_LOG_CONFIG', 'logging_config.yml')

#: Sentry DSN - will report exceptions there
SENTRY_DSN = env('SAMS_SENTRY_DSN')
SENTRY_INCLUDE_PATHS = ['sams']

# Flask/Application variables
FLASK_ENV = env('SAMS_FLASK_ENV', '')
DEBUG = strtobool(env('SAMS_DEBUG', 'false'))
SAMS_TESTING = strtobool(env('SAMS_TESTING', 'false'))

# Fix bug in Superdesk-Core/notification not using .get
CELERY_BROKER_URL = None
