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

from typing import BinaryIO, Dict, Any, List, Union, Optional
from os import path
from bson import ObjectId
from io import BytesIO
from copy import deepcopy
import PIL

from superdesk.services import Service
from superdesk.storage.mimetype_mixin import MimetypeMixin
from superdesk.storage.superdesk_file import SuperdeskFile
from superdesk.utc import utcnow
from superdesk.media.renditions import _resize_image

from sams.factory.service import SamsService
from sams.sets import get_service
from sams.utils import get_binary_stream_size, get_external_user_id

from sams_client.schemas.assets import IAsset, IAssetRendition, IAssetRenditionArgs
from sams_client.errors import SamsAssetErrors, SamsAssetImageErrors


class AssetsService(SamsService, MimetypeMixin):
    def post(self, docs: List[Dict[str, Any]], **kwargs) -> List[ObjectId]:
        """Uploads binary and stores metadata

        :param docs: An array of metadata & binaries to create
        :param kwargs: Dictionary containing the keyword arguments
        :return: list of generated IDs for the new documents
        :rtype: list[bson.objectid.ObjectId]
        """
        for doc in docs:
            doc['firstcreated'] = utcnow()
            doc['versioncreated'] = utcnow()
            external_user_id = get_external_user_id()

            if external_user_id:
                doc['original_creator'] = external_user_id
                doc['version_creator'] = external_user_id

            content = doc.pop('binary', None)

            if not content:
                raise SamsAssetErrors.BinaryNotSupplied()

            self.validate_post(doc)
            file_meta = self.upload_binary(doc, content)
            doc.update(file_meta)

            try:
                # Add original rendition to the asset renditions
                width, height = PIL.Image.open(content).size
                renditions = []
                rendition = IAssetRendition(
                    name='original',
                    _media_id=doc['_media_id'],
                    width=width,
                    height=height,
                    params=IAssetRenditionArgs(
                        width=width,
                        height=height,
                        keep_proportions=True,
                    ),
                    versioncreated=utcnow(),
                    filename=doc['filename'],
                    length=doc['length']
                )
                renditions.append(rendition)
                doc['renditions'] = renditions
            except Exception:
                pass

        return super(Service, self).post(docs, **kwargs)

    def patch(self, item_id: ObjectId, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Updates the binary and/or metadata

        .. note::
            When uploading a new binary to an existing Asset, the original binary
            will be deleted from the StorageDestination.

        :param bson.objectid.ObjectId item_id: ID for the Asset
        :param dict updates: Dictionary containing the desired metadata/binary to update
        :return: Dictionary containing the updated attributes of the Asset
        :rtype: dict
        """
        original = self.get_by_id(item_id)
        content = updates.pop('binary', None)
        self.validate_patch(original, updates)

        updates['versioncreated'] = utcnow()
        external_user_id = get_external_user_id()

        if external_user_id:
            updates['version_creator'] = external_user_id

        if content:
            asset = deepcopy(original)
            asset.update(updates)

            # Force mimetype from provided updates, if any
            asset['mimetype'] = updates.get('mimetype')

            file_meta = self.upload_binary(asset, content)
            updates.update(file_meta)

        return super(Service, self).patch(item_id, updates)

    def add_rendition(
        self,
        asset: IAsset,
        width: int,
        height: int = None,
        keep_proportions: bool = True,
        name: Optional[str] = None
    ) -> IAssetRendition:
        # Download the original image, then create the new rendition from it
        original = self.download_binary(asset['_id'])
        [rendition_binary, new_width, new_height] = _resize_image(
            original,
            (width, height),
            keepProportions=keep_proportions
        )

        # Generate a new filename which includes the dimensions
        filename, extension = path.splitext(asset['filename'])
        asset['filename'] = f'{filename}-{new_width}x{new_height}{extension}'

        # Upload the new rendition to the same StorageDestination as the original image
        upload_response = self.upload_binary(asset, rendition_binary, delete_original=False)

        # Add the rendition details to the Asset document in the DB
        renditions = asset.get('renditions') or []
        rendition = IAssetRendition(
            name=name,
            _media_id=upload_response['_media_id'],
            width=new_width,
            height=new_height,
            params=IAssetRenditionArgs(
                width=width,
                height=height,
                keep_proportions=keep_proportions,
            ),
            versioncreated=utcnow(),
            filename=asset['filename'],
            length=upload_response['length']
        )
        renditions.append(rendition)
        self.patch(ObjectId(asset['_id']), {'renditions': renditions})

        return rendition

    def get_asset_rendition_metadata(
        self,
        asset: IAsset,
        width: Optional[int] = None,
        height: Optional[int] = None,
        keep_proportions: Optional[bool] = True
    ) -> Optional[IAssetRendition]:
        return next(
            (
                rend
                for rend in asset.get('renditions') or []
                if (
                    (not width or width == (rend.get('params') or {}).get('width')) and
                    (not height or height == (rend.get('params') or {}).get('height')) and
                    keep_proportions == (rend.get('params') or {}).get('keep_proportions')
                )
            ),
            None
        )

    def download_rendition(
        self,
        asset_id: Union[ObjectId, str],
        width: Optional[int] = None,
        height: Optional[int] = None,
        keep_proportions: Optional[bool] = True
    ):
        if not width and not height:
            raise SamsAssetImageErrors.RenditionDimensionsNotProvided()

        asset: IAsset = self.get_by_id(asset_id)

        if not asset:
            raise SamsAssetErrors.AssetNotFound(asset_id)

        rendition = self.get_asset_rendition_metadata(asset, width, height, keep_proportions)

        if not rendition:
            # If the rendition does not exist, then create it now
            rendition = self.add_rendition(asset, width, height, keep_proportions)

        set_service = get_service()
        provider = set_service.get_provider_instance(asset.get('set_id'))
        asset_file = provider.get(rendition.get('_media_id'))
        asset_file.filename = asset['filename']
        return asset_file, rendition

    def on_deleted(self, doc: IAsset):
        """Delete the Asset Binary after the Metadata is deleted

        :param dict doc: The Asset that was deleted
        """

        if doc.get('_media_id'):
            set_service = get_service()
            provider = set_service.get_provider_instance(doc.get('set_id'))
            provider.delete(doc['_media_id'])

            # Make sure to also delete any renditions that were created
            for rendition in doc.get('renditions') or []:
                if rendition.get('_media_id'):
                    provider.delete(rendition['_media_id'])

    def _validate_upload_size(self, set_id: ObjectId, content: BinaryIO):
        """Validates the size of the upload against the Set or App config

        :param bson.objectid.ObjectId set_id: The ID of the Set
        :param io.BytesIO content: The binary stream
        :raises: sams_client.errors.SamsAssetErrors.AssetExceedsMaximumSizeForSet: If Asset size is too big
        """

        max_size = get_service().get_max_asset_size(set_id)

        if max_size == 0:
            return

        content_size = get_binary_stream_size(content)
        if content_size > max_size:
            raise SamsAssetErrors.AssetExceedsMaximumSizeForSet(content_size, max_size)

    def upload_binary(
        self,
        asset: Dict[str, Any],
        content: Union[BinaryIO, bytes],
        delete_original: bool = True
    ) -> dict:
        """Uploads binary data for provided Asset

        :param dict asset: The Asset Metadata used to store the binary for
        :param io.BytesIO content: The Asset Binary to upload
        :param bool delete_original: If ``True``, deletes the existing binary (if any)
        :return: Returns the ``_media_id``, ``length`` and ``mimetype`` attributes of the binary
        :rtype: dict
        """

        set_id = asset.get('set_id')
        filename = asset.get('filename')

        # Seek the buffer to the beginning
        # If `seek` is not available, then we have received an instance of `bytes`
        # so convert it to an `io.BytesIO` instance
        try:
            content.seek(0)
        except AttributeError:
            content = BytesIO(content)

        mimetype = self._get_mimetype(content, filename, asset.get('mimetype'))

        content.seek(0)

        self._validate_upload_size(set_id, content)

        set_service = get_service()
        provider = set_service.get_provider_instance(set_id)
        media_id = provider.put(content, filename, mimetype)

        asset_binary = provider.get(media_id)

        if delete_original and asset.get('_media_id'):
            provider.delete(asset['_media_id'])

        return {
            'binary': media_id,
            '_media_id': media_id,
            'length': asset_binary.length,
            'mimetype': mimetype
        }

    def download_binary(self, asset_id: Union[ObjectId, str]) -> SuperdeskFile:
        """Downloads the Asset Binary

        :param bson.objectid.ObjectId asset_id: The ID of the Asset
        :return: The Binary Stream for the Asset Binary
        :rtype: superdesk.storage.superdesk_file.SuperdeskFile
        """

        asset = self.get_by_id(asset_id)
        if not asset:
            raise SamsAssetErrors.AssetNotFound(asset_id)

        set_service = get_service()
        provider = set_service.get_provider_instance(asset.get('set_id'))
        asset_file = provider.get(asset.get('_media_id'))
        asset_file.filename = asset['filename']
        return asset_file
