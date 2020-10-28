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

from typing import BinaryIO
from os import SEEK_END


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
