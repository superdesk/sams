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

import logging
import logging.config
import yaml
from os import path

SAMS_DIR = path.abspath(path.join(path.dirname(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sams')

# set default levels
logging.getLogger('kombu').setLevel(logging.WARNING)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.INFO)
logging.getLogger('superdesk').setLevel(logging.INFO)

logging.getLogger('sams').setLevel(logging.INFO)


def configure_logging(file_path):
    if not file_path:
        logger.warning('file_path not defined')
        return
    elif not path.exists(file_path):
        if not path.exists(path.join(SAMS_DIR, file_path)):
            logger.error('file_path "%s" not found', file_path)
            return

        file_path = path.join(SAMS_DIR, file_path)

    try:
        with open(file_path, 'r') as f:
            logging_dict = yaml.load(f)

        logging.config.dictConfig(logging_dict)

        logger.debug('Logging configured')
    except Exception as e:
        logger.warning(
            'Cannot load logging config. File: %s, Error: %s',
            file_path,
            str(e)
        )
