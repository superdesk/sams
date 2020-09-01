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

"""The Sets Consume API allows to search Sets.

This service and resource is intended to be used by external clients.
To access Sets inside the SAMS application, use the :mod:`sams.sets` module instead

=====================   =========================================================
**endpoint name**        'consume_sets'
**resource title**       'Set'
**resource url**         [GET] '/consume/sets'
**item url**             [GET] '/consume/sets/<:class:`~bson.objectid.ObjectId`>'
**schema**               :attr:`sams_client.schemas.sets.SET_SCHEMA`
=====================   =========================================================
"""

from superdesk.resource import Resource, build_custom_hateoas

from sams.api.service import SamsApiService


class ConsumeSetResource(Resource):
    endpoint_name = 'consume_sets'
    resource_title = 'Set'
    url = 'consume/sets'
    item_methods = ['GET']
    resource_methods = ['GET']
    allow_unknown = True


class ConsumeSetService(SamsApiService):
    def on_fetched_item(self, doc):
        self.enhance_items([doc])

    def on_fetched(self, doc):
        self.enhance_items(doc['_items'])

    def enhance_items(self, docs):
        for doc in docs:
            build_custom_hateoas(
                {
                    'self': {
                        'title': ConsumeSetResource.resource_title,
                        'href': ConsumeSetResource.url + '/{_id}'
                    }
                },
                doc,
                _id=str(doc.get('_id'))
            )
