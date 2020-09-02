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

"""The Sets Admin API allows to create, update or delete Sets.

This service and resource is intended to be used by external clients.
To access Sets inside the SAMS application, use the :mod:`sams.sets` module instead

=====================   =================================================================
**endpoint name**        'admin_sets'
**resource title**       'Set'
**resource url**         [POST] '/admin/sets'
**item url**             [PATCH, DELETE] '/admin/sets/<:class:`~bson.objectid.ObjectId`>'
**schema**               :attr:`sams_client.schemas.sets.SET_SCHEMA`
=====================   =================================================================
"""

from superdesk.resource import Resource, build_custom_hateoas

from sams.api.service import SamsApiService
from sams.api.consume.sets import ConsumeSetResource


class AdminSetResource(Resource):
    endpoint_name = 'admin_sets'
    resource_title = 'Set'
    url = 'admin/sets'
    item_methods = ['PATCH', 'DELETE']
    resource_methods = ['POST']
    allow_unknown = True


class AdminSetService(SamsApiService):
    def on_created(self, docs):
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
