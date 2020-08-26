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

"""
The :class:`SamsApiService` provides the base service for APIs to proxy requests to
internal services.

Here you will find an example usage of the :class:`SamsApiService` to add a new endpoint
to the API. all::

    from superdesk import get_resource_service
    from superdesk.resource import Resource
    from sams.factory.app import SamsApp
    from sams.api.service import SamsApiService

    class ApiTestResource(Resource):
        endpoint_name = 'test_resource'
        resource_title = 'test resource'
        url = '/consume/test'
        item_methods = ['GET']
        resource_methods = ['GET']
        schema = {...}

    class ApiTestService(SamsApiService):
        pass

    def init_app(app: SamsApp):
        ApiTestResource(
            endpoint_name=ApiTestResource.endpoint_name,
            app=app,
            service=ApiTestService(
                get_resource_service('internal_service_name')
            )
        )
"""

from typing import Dict, List, Any

from eve.utils import ParsedRequest
from flask import json
from bson import ObjectId
from pymongo.cursor import Cursor as MongoCursor
from eve_elastic.elastic import ElasticCursor

from superdesk.services import BaseService

from sams_client.errors import SamsSystemErrors
from sams.factory.service import SamsService


class SamsApiService(SamsService):
    """Sams API Service

    Base service for external API endpoints that proxy requests to internal services.

    :var BaseService service: The service to proxy requests to
    """

    def __init__(self, service: BaseService):
        self.service: BaseService = service
        super().__init__()

    def _remove_system_attributes(self, doc: Dict[str, Any]):
        """Removes system attributes from the document

        This will remove ``_created``, ``_updated`` and ``_etag``. The attached
        internal service will be in charge of populating these attributes

        :param dict doc: The document to strip system attributes from
        """

        doc.pop('_created', None)
        doc.pop('_updated', None)
        doc.pop('_etag', None)

    def create(self, docs: List[Dict[str, Any]], **kwargs) -> List[ObjectId]:
        """Proxy method to create a new document

        Removes system attributes using :meth:`_remove_system_attributes`.
        Then passes the request to the :meth:`sams.factory.service.SamsService.post`
        method of the underlying service.

        :param list[dict] docs: The list of documents to be created
        :param dict kwargs: Extra arguments to pass onto the underlying service
        :rtype: list[bson.objectid.ObjectId]
        :return: list og generated IDs for the new documents
        """

        for doc in docs:
            self._remove_system_attributes(doc)

        return self.service.post(docs, **kwargs)

    def update(self, id: ObjectId, updates: Dict[str, Any], original: Dict[str, Any]) -> Dict[str, Any]:
        """Proxy method to update an existing document

        Removes system attributes using :meth:`_remove_system_attributes`.
        Then passes the request to the :meth:`sams.factory.service.SamsService.patch`
        method of the underlying service

        :param bson.objectid.ObjectId id: ID for the document
        :param dict updates: Dictionary containing the desired attributes to update
        :param dict original: Dictionary containing the original document
        :rtype: dict
        :return: dictionary containing the updated attributes of the document
        """

        self._remove_system_attributes(updates)

        return self.service.patch(id, updates)

    def system_update(self, id: ObjectId, updates: Dict[str, Any], original: Dict[str, any]):
        """Not to be used with API Service

        :raises superdesk.errors.SuperdeskApiError:
        """

        raise SamsSystemErrors.SystemUpdateNotAllowed()

    def replace(self, id: ObjectId, document: Dict[str, Any], original: Dict[str, Any]) -> Dict[str, Any]:
        """Replaces an existing document with a new one

        Passes the request to the :meth:`sams.factory.service.SamsService.replace` method.

        :param bson.objectid.ObjectId id: ID of the document to replace
        :param dict document: Dictionary containing the original document
        :param dict original: Dictionary containing the new document
        :rtype: dict
        :return: dictionary containing the new document
        """

        return self.service.replace(id, document, original)

    def delete(self, lookup: Dict[str, Any]):
        """Deletes documents based on a lookup query

        Passes the request to the :meth:`sams.factory.service.SamsService.delete` method.

        :param dict lookup: Lookup used to determine what documents to delete
        :return: The response of the delete action
        """

        return self.service.delete_action(lookup)

    def delete_ids_from_mongo(self, ids: List[ObjectId]):
        """Deletes documents in mongo based on their IDs

        Passes the request to the :meth:`sams.factory.service.SamsService.delete_ids_from_mongo` method.

        :param list[bson.objectid.ObjectId] ids: The list of IDs to delete
        :return: The response of the delete action
        """

        return self.service.delete_ids_from_mongo(ids)

    def delete_docs(self, docs: List[Dict[str, Any]]):
        """Deletes documents

        Passes the request to the :meth:`sams.factory.service.SamsService.delete_docs` method.

        :param list[dict] docs: The list of documents to delete
        :return: The response of the delete action
        """

        return self.service.delete_docs(docs)

    def find_one(self, req: ParsedRequest, **lookup) -> Dict[str, Any]:
        """Finds a single document based on request and lookup args

        Passes the request to the :meth:`sams.factory.service.SamsService.find_one` method.

        :param eve.utils.ParsedRequest req: The request object
        :param dict lookup: Dictionary containing optional lookup arguments
        :rtype: dict
        :return: The document if found
        """

        return self.service.find_one(req=req, **lookup)

    def find(self, where: Dict[str, Any], **kwargs) -> MongoCursor or ElasticCursor:
        """Find documents using the provided query arguments

        Passes the request to the :meth:`sams.factory.service.SamsService.find` method.

        :param dict where: Dictionary containing query parameters
        :param dict kwargs: Dictionary containing optional lookup arguments
        :rtype: pymongo.cursor.MongoCursor | eve_elastic.elastic.ElasticCursor
        :return: A Mongo or Elastic cursor with the results
        """

        return self.service.find(where, **kwargs)

    def get(self, req: ParsedRequest, lookup: Dict[str, Any]):
        """Find documents using the provided query arguments

        Passes the request to the :meth:`sams.factory.service.SamsService.get` method;

        :param eve.utils.ParsedRequest req: The request object
        :param dict lookup: Dictionary containing optional lookup arguments
        :rtype: pymongo.cursor.MongoCursor | eve_elastic.elastic.ElasticCursor
        :return: A Mongo or Elastic cursor with the results
        """

        if req is None:
            req = ParsedRequest()
        return self.service.get(req=req, lookup=lookup)

    def get_from_mongo(
        self,
        req: ParsedRequest,
        lookup: Dict[str, Any],
        projection: Dict[str, Any] = None
    ) -> MongoCursor:
        """Find documents using MongoDB.

        Passes the request to the :meth:`sams.factory.service.SamsService.get_from_mongo` method.

        :param eve.utils.ParsedRequest req: The request object
        :param dict lookup: Dictionary containing optional lookup arguments
        :param dict projection: Dictionary containing optional projection
        :rtype: pymongo.cursor.MongoCursor
        :return: A Mongo cursor with the results
        """

        if req is None:
            req = ParsedRequest()
        if not req.projection and projection:
            req.projection = json.dumps(projection)
        return self.service.get_from_mongo(req=req, lookup=lookup)

    def find_and_modify(self, **kwargs):
        """Find and modify documents

        Passes the request to the :meth:`sams.factory.service.SamsService.find_and_modify` method.

        :param kwargs:
        :return: The response of the request
        """

        return self.service.find_and_modify(**kwargs)

    def search(self, source: Dict[str, Any]) -> ElasticCursor:
        """Find documents using Elasticsearch

        Passes the request to the :meth:`sams.factory.service.SamsService.search` method.

        :param dict source: The source query to pass to Elasticsearch
        :rtype: ElasticCursor
        :return: An Elasticsearch cursor with the results
        """

        return self.service.search(source)

    def remove_from_search(self, item: Dict[str, Any]):
        """Removes a document from Elasticsearch only

        Passes the request to the :meth:`sams.factory.service.SamsService.remove_from_search` method.

        :param dict item: The document to remove
        """

        return self.service.remove_from_search(item)
