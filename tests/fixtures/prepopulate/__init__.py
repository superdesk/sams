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

from flask import current_app as app, request

from superdesk import get_resource_service
from superdesk.resource import Resource
from superdesk.services import Service

from sams.factory.app import SamsApp
from sams.storage.destinations import destinations
from sams.storage.providers import providers


class PrepopulateResource(Resource):
    url = 'tests/prepopulate'
    endpoint_name = 'tests/prepopulate'

    schema = {
        'method': {
            'type': 'string',
            'required': True,
            'default': 'reset'
        },
        'args': {
            'type': 'dict',
            'allow_unknown': True
        }
    }

    item_methods = []
    resource_methods = ['POST']


class PrepopulateService(Service):
    def create(self, docs, **kwargs):
        for doc in docs:
            try:
                method_name = doc['method']
            except Exception:
                method_name = 'reset'

            method = getattr(self, method_name)
            method(doc.get('args') or {})

        return ['OK']

    def reset(self, args):
        app.data.init_elastic(app)
        self.clean_databases()

    def add(self, args):
        resource = args.get('resource')
        docs = args.get('docs')

        get_resource_service(resource).post(docs)

    def shutdown(self, args):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def clean_databases(self):
        app.data.mongo.pymongo().cx.drop_database(app.config['MONGO_DBNAME'])
        indices = '%s*' % app.config['ELASTICSEARCH_INDEX']
        es = app.data.elastic.es
        es.indices.delete(indices, ignore=[404])
        with app.app_context():
            app.data.init_elastic(app)

    def clean_storage_config(self):
        destinations.clear()
        providers.clear()


def init_app(app: SamsApp):
    PrepopulateResource(
        endpoint_name=PrepopulateResource.endpoint_name,
        app=app,
        service=PrepopulateService(PrepopulateResource.endpoint_name, backend=None)
    )
