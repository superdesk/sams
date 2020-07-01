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

from os import path, getcwd, environ
from importlib import import_module

from flask import Config, jsonify
from werkzeug.exceptions import HTTPException
from eve import Eve
from eve.io.mongo import MongoJSONEncoder

from superdesk.datalayer import SuperdeskDataLayer
from superdesk.errors import SuperdeskApiError
from superdesk.notification import ClosedSocket
from superdesk.validator import SuperdeskValidator

from sams.logging import configure_logging, logger

SAMS_DIR = path.abspath(path.join(path.dirname(__file__), '..'))


def is_json_request(request):
    """Test if request is for json content."""
    return request.args.get('format') == 'json' or \
        request.accept_mimetypes.best_match(['application/json', 'text/html']) == 'application/json'


class SamsApp(Eve):
    """The base Newsroom object.

    Usage::

        from sams.factory import get_app

        app = get_app(__name__, config={...})
        app.run()
    """

    def __init__(self, import_name=__package__, config=None, **kwargs):
        """Override __init__ to do SAMS specific config and still be able
        to create an instance using ``app = SamsApp()``
        """

        super(SamsApp, self).__init__(
            import_name,
            data=SuperdeskDataLayer,
            json_encoder=MongoJSONEncoder,
            validator=SuperdeskValidator,
            **kwargs
        )
        self.json_encoder = MongoJSONEncoder

        if config:
            try:
                self.config.update(config or {})
            except TypeError:
                self.config.from_object(config)

        self.setup_logging()
        self.config['RENDERERS'] = ['eve.render.JSONRenderer']
        self.setup_auth()
        self.setup_error_handlers()

        if self.config.get('CORE_APPS'):
            self.setup_apps(self.config['CORE_APPS'])

        if self.config.get('INSTALLED_APPS'):
            self.setup_apps(self.config.get('INSTALLED_APPS', []))

        # Mock sending websocket notifications
        # As parts of superdesk-core depends on this (i.e. resource:updated)
        self.notification_client = ClosedSocket()

    def load_app_config(self):
        self.config.from_object('sams.default_settings')

        try:
            self.config.from_pyfile(path.join(getcwd(), 'settings.py'))
        except FileNotFoundError:
            pass

    def load_config(self):
        # Override Eve.load_config in order to get default_settings

        if not getattr(self, 'settings'):
            self.settings = Config('.')

        super(SamsApp, self).load_config()
        self.config.setdefault('DOMAIN', {})
        self.config.setdefault('SOURCES', {})
        self.load_app_config()

    def setup_error_handlers(self):
        def json_error(err):
            return jsonify(err), err['code']

        def handle_werkzeug_errors(err):
            logger.exception(err)
            return json_error({
                'error': str(err),
                'message': getattr(err, 'description') or None,
                'code': getattr(err, 'code') or 500
            })

        def superdesk_api_error(err):
            logger.exception(err)
            return json_error({
                'error': err.message or '',
                'message': getattr(err, 'payload', err.message),
                'code': err.status_code or 500,
            })

        def assertion_error(err):
            logger.exception(err)
            return json_error({
                'error': err.args[0] if err.args else 1,
                'message': str(err),
                'code': 400
            })

        def base_exception_error(err):
            logger.exception(err)
            if getattr(err, 'error', None) == 'search_phase_execution_exception':
                return json_error({
                    'error': 1,
                    'message': 'Invalid search query',
                    'code': 400
                })

            return json_error({
                'error': err.args[0] if err.args else 1,
                'message': str(err),
                'code': 500
            })

        for cls in HTTPException.__subclasses__():
            self.register_error_handler(cls, handle_werkzeug_errors)

        self.register_error_handler(SuperdeskApiError, superdesk_api_error)
        self.register_error_handler(AssertionError, assertion_error)
        self.register_error_handler(Exception, base_exception_error)

    def setup_apps(self, apps):
        """Setup configured apps."""
        for name in apps:
            mod = import_module(name)
            if hasattr(mod, 'init_app') and callable(mod.init_app):
                mod.init_app(self)

    def setup_auth(self):
        if not self.config.get('SAMS_AUTH_TYPE'):
            raise RuntimeError('Auth type not specified')

        mod = import_module(self.config['SAMS_AUTH_TYPE'])
        if not hasattr(mod, 'get_auth_instance') or not callable(mod.get_auth_instance):
            raise RuntimeError('Configured Auth type must have a `get_auth_instance` method')

        api_keys = self.config.get('CLIENT_API_KEYS').split(',')
        self.auth = mod.get_auth_instance(api_keys=api_keys)

    def setup_logging(self):
        if self.config.get('LOG_CONFIG_FILE'):
            configure_logging(self.config['LOG_CONFIG_FILE'])
