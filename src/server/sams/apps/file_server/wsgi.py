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

from .app import get_app

application = get_app(__name__)


if __name__ == '__main__':
    application.run(
        host=application.config['HOST'],
        port=application.config['PORT'],
        debug=application.config['DEBUG'],
        use_reloader=application.config['DEBUG']
    )
