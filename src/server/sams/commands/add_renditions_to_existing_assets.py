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
import PIL
from sams.assets import get_service as get_asset_service
from sams_client.schemas.assets import IAssetRendition, IAssetRenditionArgs
from sams.logger import logger

from superdesk.utc import utcnow
from superdesk import Command, command


class AddOriginalRenditions(Command):
    """Add Original Rendition

    It adds original rendition to existing assets without original rendition.
    It also adds names of renditions to existing asset renditions without name, for ex. thumbnail, viewImage

    Example:
    ::

        $ python -m sams.manage app:add_original_renditions

    """

    def run(self):
        logger.info('Add Original Renditions to existing assets')
        self.add_original_rendition()

    @classmethod
    def add_original_rendition(cls):
        """Adds original rendition to the existing assets
        """

        service = get_asset_service()
        db_assets = app.data.get_mongo_collection('assets').find()
        assets_without_original_rendition = []
        for asset in db_assets:
            renditions = asset.get('renditions', [])
            for rendition in renditions:
                if not rendition.get('name'):
                    assets_without_original_rendition.append(asset)
                    break

        for asset in assets_without_original_rendition:
            updates = {}
            updates['renditions'] = []

            original = service.download_binary(asset['_id'])

            try:
                width, height = PIL.Image.open(original).size
                rendition = IAssetRendition(
                    name='original',
                    _media_id=asset['_media_id'],
                    width=width,
                    height=height,
                    params=IAssetRenditionArgs(
                        width=width,
                        height=height,
                        keep_proportions=True,
                    ),
                    versioncreated=utcnow(),
                    filename=asset['filename'],
                    length=asset['length']
                )
                updates['renditions'].append(rendition)
            except Exception:
                pass

            for rendition in asset['renditions']:
                if rendition['params']['width'] == 220:
                    rendition['name'] = 'thumbnail'
                    updates['renditions'].append(rendition)

                if rendition['params']['width'] == 640:
                    rendition['name'] = 'viewImage'
                    updates['renditions'].append(rendition)

            get_asset_service().system_update(asset['_id'], {'renditions': updates['renditions']}, asset)


command('app:add_original_renditions', AddOriginalRenditions())
