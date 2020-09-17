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
from superdesk import Command, command, Option

from sams.logger import logger

from .delete_elastic_index import DeleteElasticIndex
from .index_from_mongo import IndexFromMongo

# this one is not configurable
SAMS_ELASTIC_PREFIX = 'ELASTICSEARCH'


class FlushElasticIndex(Command):
    """Flush elastic index.

    It removes elastic index, creates a new one and index it from mongo.

    ===============   ======   ===============================================
    **--page-size**   **-p**   Size of every list in each iteration
    ===============   ======   ===============================================

    Example:
    ::

        $ python -m sams.manage app:flush_elastic_index
        $ python -m sams.manage app:flush_elastic_index --page-size=100

    """

    option_list = [
        Option('--page-size', '-p', type=int, default=500)
    ]

    def run(self, page_size):
        logger.info('Flushing elastic index')
        DeleteElasticIndex.delete_elastic(app.config['ELASTICSEARCH_INDEX'])
        self._index_from_mongo(page_size)

    def _index_from_mongo(self, page_size):
        """Index elastic search from mongo.

        :param page_size: Size of every list in each iteration
        """

        # get all es resources
        app.data.init_elastic(app)
        resources = app.data.get_elastic_resources()

        for resource in resources:
            # get es prefix per resource
            es_backend = app.data._search_backend(resource)
            resource_es_prefix = es_backend._resource_prefix(resource)

            if resource_es_prefix == SAMS_ELASTIC_PREFIX:
                logger.info(
                    'Indexing mongo collections into "%s" elastic index.',
                    app.config['ELASTICSEARCH_INDEX']
                )
                IndexFromMongo.copy_resource(
                    resource,
                    page_size
                )


command('app:flush_elastic_index', FlushElasticIndex())
