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
from eve_elastic import get_es
from elasticsearch import exceptions as es_exceptions

from superdesk import Command, command

from sams.logger import logger


class DeleteElasticIndex(Command):
    """Delete elastic index

    It removes all elastic indices.

    Example:
    ::

        $ python -m sams.manage app:delete_elastic_index

    """

    def run(self):
        logger.info('Delete elastic indices')
        self.delete_elastic(app.config['ELASTICSEARCH_INDEX'])

    @classmethod
    def delete_elastic(cls, index_prefix):
        """Deletes elastic indices with `index_prefix`

        :param str index_prefix: elastix index
        :raise: SystemExit exception if delete elastic index response status is not 200 or 404.
        """

        es = get_es(app.config['ELASTICSEARCH_URL'])
        indices = list(es.indices.get_alias('{}_*'.format(index_prefix)).keys())

        for es_resource in app.data.get_elastic_resources():
            alias = app.data.elastic._resource_index(es_resource)
            for index in indices:
                if index.rsplit('_', 1)[0] == alias:
                    try:
                        logger.info('Removing elastic index "%s"', index)
                        es.indices.delete(index=index)
                    except es_exceptions.NotFoundError:
                        logger.warning('"%s" elastic index was not found. Continue without deleting.', index)
                    except es_exceptions.TransportError as e:
                        raise SystemExit(
                            '"{}" elastic index was not deleted. Exception: "{}"'.format(index, e.error))
                    else:
                        logger.info('"%s" elastic index was deleted.', index)
                        break


command('app:delete_elastic_index', DeleteElasticIndex())
