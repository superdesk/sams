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

from eve import Eve
from werkzeug.exceptions import HTTPException

from sams.logger import logger
from sams_client.errors import SamsException, SamsHTTPError, SamsSystemErrors, SamsResourceErrors


def sams_api_error(err: SamsException):
    if getattr(err, 'log_exception', False):
        logger.exception(err)

        # If an internal exception is attached to this exception
        # then log that exception as well
        if getattr(err, 'exception', None):
            logger.exception(err.exception)

    return err.to_error_response()


def handle_werkzeug_errors(err):
    return sams_api_error(
        SamsHTTPError(err)
    )


def assertion_error(err):
    return sams_api_error(
        SamsSystemErrors.AssertionError(str(err), err)
    )


def not_implemented_error(err):
    return sams_api_error(
        SamsSystemErrors.NotImplemented(str(err), err)
    )


def base_exception_error(err):
    if getattr(err, 'error', None) == 'search_phase_execution_exception':
        return sams_api_error(
            SamsResourceErrors.InvalidSearchQuery()
        )

    return sams_api_error(
        SamsSystemErrors.UnknownError(str(err), err)
    )


def setup_error_handlers(app: Eve):
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, handle_werkzeug_errors)

    app.register_error_handler(SamsException, sams_api_error)
    app.register_error_handler(AssertionError, assertion_error)
    app.register_error_handler(NotImplementedError, not_implemented_error)
    app.register_error_handler(Exception, base_exception_error)
