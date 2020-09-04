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

import time
import pymongo
from flask import current_app as app

from superdesk import Command, command, Option, config
from superdesk.errors import BulkIndexError

from sams.logger import logger


class IndexFromMongo(Command):
    """Index the specified mongo collection in the specified elastic collection/type.

    This will use the default APP mongo DB to read the data and the default Elastic APP index.

    Use ``-f all`` to index all collections.

    Example:
    ::

        $ python -m sams.manage app:index_from_mongo --from=assets
        $ python -m sams.manage app:index_from_mongo --all

    """

    option_list = [
        Option('--from', '-f', dest='collection_name'),
        Option('--all', action='store_true', dest='all_collections'),
        Option('--page-size', '-p')
    ]
    default_page_size = 500

    def run(self, collection_name, all_collections, page_size):
        if not collection_name and not all_collections:
            raise SystemExit('Specify --all to index from all collections')
        elif all_collections:
            app.data.init_elastic(app)
            resources = app.data.get_elastic_resources()
            for resource in resources:
                self.copy_resource(resource, page_size)
        else:
            self.copy_resource(collection_name, page_size)

    @classmethod
    def copy_resource(cls, resource, page_size):
        for items in cls.get_mongo_items(resource, page_size):
            logger.info('{} Inserting {} items'.format(time.strftime('%X %x %Z'), len(items)))
            s = time.time()
            success, failed = 0, 0

            for i in range(1, 4):
                try:
                    success, failed = app.data._search_backend(resource).bulk_insert(
                        resource, items)
                except Exception as ex:
                    logger.exception('Exception thrown on insert to elastic {}', ex)
                    time.sleep(10)
                    continue
                else:
                    break

            logger.info('{} Inserted {} items in {:.3f} seconds'.format(time.strftime('%X %x %Z'), success, time.time() - s))
            if failed:
                logger.error('Failed to do bulk insert of items {}. Errors: {}'.format(len(failed), failed))
                raise BulkIndexError(resource=resource, errors=failed)

        return 'Finished indexing collection {}'.format(resource)

    @classmethod
    def get_mongo_items(cls, mongo_collection_name, page_size):
        """Generate list of items from given mongo collection per page size.

        :param mongo_collection_name: Name of the collection to get the items
        :param page_size: Size of every list in each iteration
        :return: list of items
        """
        bucket_size = int(page_size) if page_size else cls.default_page_size
        logger.info('Indexing data from mongo/{} to elastic/{}'.format(mongo_collection_name, mongo_collection_name))

        db = app.data.get_mongo_collection(mongo_collection_name)
        args = {'limit': bucket_size, 'sort': [(config.ID_FIELD, pymongo.ASCENDING)]}
        last_id = None
        while True:
            if last_id:
                args.update({'filter': {config.ID_FIELD: {'$gt': last_id}}})
            cursor = db.find(**args)
            if not cursor.count():
                break
            items = list(cursor)
            last_id = items[-1][config.ID_FIELD]
            yield items


command('app:index_from_mongo', IndexFromMongo())