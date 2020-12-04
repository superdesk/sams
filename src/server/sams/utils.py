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

from typing import BinaryIO, Dict, Any

from os import SEEK_END
import hashlib

from flask import request, current_app as app, Response
from werkzeug.wsgi import wrap_file

from superdesk.storage.superdesk_file import SuperdeskFile

from sams.default_settings import strtobool


def get_binary_stream_size(content: BinaryIO) -> int:
    """Gets the size in bytes of the binary stream

    :param io.BytesIO content: The binary stream to inspect
    :return: The size in bytes of the stream
    :rtype: int
    """

    content.seek(0, SEEK_END)
    content_size = content.tell()
    content.seek(0)
    return content_size


def construct_asset_download_response(
    asset: Dict[str, Any],
    file: SuperdeskFile,
    cache_for: int = None,
    buffer_size: int = None
) -> Response:
    if buffer_size is None:
        buffer_size = 1024 * 256

    if cache_for is None:
        cache_for = 3600 * 24 * 30  # 30d cache

    data = wrap_file(request.environ, file, buffer_size=buffer_size)
    response = app.response_class(
        data,
        mimetype=asset['mimetype'],
        direct_passthrough=True
    )
    response.content_length = asset['length']
    response.last_modified = asset['_updated']
    h = hashlib.sha1()
    h.update(file.read())
    file.seek(0)
    response.set_etag(h.hexdigest())
    response.cache_control.max_age = cache_for
    response.cache_control.s_max_age = cache_for
    response.cache_control.public = True
    response.make_conditional(request)

    if strtobool(request.args.get('download', 'False')):
        response.headers['Content-Disposition'] = 'Attachment; filename={}'.format(asset['filename'])
    else:
        response.headers['Content-Disposition'] = 'Inline; filename={}'.format(asset['filename'])

    return response


def get_external_user_id() -> str:
    return request.args.get('external_user_id')


def get_external_session_id() -> str:
    return request.args.get('external_session_id')
