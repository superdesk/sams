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

from flask import current_app as app
from superdesk import Command, command

from sams.logger import logger

from .delete_elastic_index import DeleteElasticIndex
from .index_from_mongo import IndexFromMongo

# this one is not configurable
SAMS_ELASTIC_PREFIX = 'ELASTICSEARCH'


class FlushElasticIndex(Command):
    """Flush elastic index.

    It removes elastic index, creates a new one and index it from mongo.

    Example:
    ::

        $ python -m sams.manage app:flush_elastic_index

    """

    def run(self):
        logger.info('Flushing elastic index')
        DeleteElasticIndex.delete_elastic(app.config['ELASTICSEARCH_INDEX'])
        self._index_from_mongo()

    def _index_from_mongo(self):
        """Index elastic search from mongo.

        """
        # get all es resources
        app.data.init_elastic(app)
        resources = app.data.get_elastic_resources()

        for resource in resources:
            # get es prefix per resource
            es_backend = app.data._search_backend(resource)
            resource_es_prefix = es_backend._resource_prefix(resource)

            if resource_es_prefix == SAMS_ELASTIC_PREFIX:
                logger.info('Indexing mongo collections into "{}" elastic index.'.format(
                    app.config['ELASTICSEARCH_INDEX'])
                )
                IndexFromMongo.copy_resource(
                    resource,
                    IndexFromMongo.default_page_size
                )


command('app:flush_elastic_index', FlushElasticIndex())
