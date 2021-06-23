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

"""Amazon S3 Storage Provider

This provider is enabled by default in the ``STORAGE_PROVIDERS`` config.
If you need to override this default, make sure to include AmazonS3Provider.
For example::

    STORAGE_PROVIDERS = [
        'sams.storage.providers.amazon.AmazonS3Provider'
    ]

This will then allow destinations to be configured for Sets to use. For example::

    STORAGE_DESTINATION_1 = 'AmazonS3,Default,access=access123,secret=secret456,region=eu-west-3,bucket=test'

The following is a list of the supported config attributes

=====================   ======================================================================
**Attribute Name**      Description
=====================   ======================================================================
access*                 Access key ID for authentication
secret*                 Secret key for authentication
region*                 Amazon region to use
bucket*                 The name of the bucket to use
endpoint_url            The Amazon endpoint url
folder                  An optional folder to use
=====================   ======================================================================

[*] Indicates required config attributes

"""

from typing import Optional, BinaryIO, Union
from os.path import splitext
from urllib.parse import urlparse

import unidecode
import logging

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from bson import ObjectId

from superdesk.media.media_operations import guess_media_extension
from superdesk.storage.amazon_media_storage import AmazonObjectWrapper

from .base import SamsBaseStorageProvider
from sams_client.errors import SamsAssetErrors, SamsAmazonS3Errors

logger = logging.getLogger(__name__)

MAX_KEYS = 1000


class AmazonS3Config:
    """Utility class to store the AmazonS3 Config

    :var str access_key: Access key ID for authentication
    :var str secret: Secret key for authentication
    :var str region: Amazon region to use
    :var str bucket: The name of the bucket to use
    :var str endpoint_url: Optional Amazon endpoint url
    :var str folder: Optional folder to use
    """

    access_key: str = None
    secret: str = None
    region: str = None
    bucket: str = None
    endpoint_url: Optional[str] = None
    folder: Optional[str] = None

    def __init__(self, config_string: str):
        """Convert config string to dictionary of key/value pairs

        i.e. converts 'access=access123,secret=secret456'
        to {'access': 'access123', 'secret': 'secret456'}
        """

        try:
            options = {
                key: value
                for key, value in [
                    entry.split('=')
                    for entry in config_string.split(',')
                ]
            }

            # Required config attributes
            self.access_key = options['access']
            self.secret = options['secret']
            self.region = options['region']
            self.bucket = options['bucket']

            # Optional config attributes
            self.endpoint_url = options.get('endpoint', None)
            self.folder = options.get('folder', None)
        except KeyError as ex:
            # Required config attribute is missing
            raise SamsAmazonS3Errors.MissingAmazonConfig(ex.args[0], ex)
        except Exception as ex:
            # Unknown config error occurred
            raise SamsAmazonS3Errors.InvalidAmazonDestinationConfig(config_string, ex)


class AmazonS3Provider(SamsBaseStorageProvider):
    """Provides storage to/from Amazon S3

    :var AmazonS3Config _config: The S3 config
    :var boto3.client _client: The Amazon client instance
    :var str type_name: The type name used to identify this provider - ``AmazonS3``
    """

    type_name = 'AmazonS3'

    def __init__(self, config_str: str):
        super(AmazonS3Provider, self).__init__(config_str)

        self._config = AmazonS3Config(self.config_string)
        self._client = self._connect_client()

    def _connect_client(self):
        """Constructs a new S3 client instance

        :return: A new S3 client instance
        :rtype: boto3.client
        """

        try:
            return boto3.client(
                's3',
                aws_access_key_id=self._config.access_key,
                aws_secret_access_key=self._config.secret,
                region_name=self._config.region,
                config=Config(signature_version='s3v4'),
                endpoint_url=self._config.endpoint_url,
            )
        except Exception as ex:
            self._raise_amazon_exception(ex)

    def _get_key(self, media_id: str):
        """Prefix the media id with the folder, if used

        :param str media_id: The media_id stored in Assets DB
        :return: The full key as used in S3
        :rtype: str
        """

        folder = self._config.folder
        if media_id and folder:
            media_id = '%s/%s' % (folder.strip('/'), media_id)
        return self._make_s3_safe(media_id)

    def _make_s3_safe(self, media_id: str):
        """Removes characters from the input _id that may cause issues when using the string as a key in S3 storage.

        See https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html

        :param str media_id: The media_id stored in Assets DB
        :return: A safe key for use with S3
        :rtype: str
        """

        def get_translation_table():
            return ''.maketrans({
                '\\': '',
                '{': '',
                '^': '',
                '}': '',
                '%': '',
                '`': '',
                ']': '',
                '>': '',
                '[': '',
                '~': '',
                '<': '',
                '#': '',
                '|': '',
                "'": '',
                '"': ''
            })

        return unidecode.unidecode(str(media_id)).translate(get_translation_table())

    def _generate_key(self, filename: str, mimetype: str):
        """Generates a unique key based on filename and mimetype

        Combines the ``filename`` and an ``ObjectId`` to generate a unique key for S3.
        ``{filename}-{ObjectId}.{extension}``

        :param str filename: The filename to use
        :param str mimetype: The mimetype (used to guess the extension)
        :return: The key to use with S3
        :rtype: str
        """

        path = urlparse(filename).path
        file_name, file_extension = splitext(path)

        if not file_extension:
            file_extension = str(guess_media_extension(mimetype)) if mimetype else ''

        return '%s-%s%s' % (
            self._make_s3_safe(file_name),
            str(ObjectId()),
            file_extension
        )

    def _raise_amazon_exception(self, exception: Exception, **kwargs):
        """Inspects type of Exception and raises SAMS error"""

        if isinstance(exception, ValueError) and str(exception).startswith('Invalid endpoint'):
            raise SamsAmazonS3Errors.InvalidAmazonEndpoint(exception=exception)
        elif isinstance(exception, ClientError):
            error_code = (exception.response.get('Error') or {}).get('Code')

            if not error_code:
                return
            elif error_code == 'InvalidAccessKeyId':
                raise SamsAmazonS3Errors.InvalidAccessKeyId(exception=exception)
            elif error_code == 'SignatureDoesNotMatch':
                raise SamsAmazonS3Errors.InvalidSecret(exception=exception)
            elif error_code == 'NoSuchBucket':
                raise SamsAmazonS3Errors.BucketNotFound(self._config.bucket, exception)
            elif error_code == 'BucketAlreadyOwnedByYou':
                raise SamsAmazonS3Errors.BucketAlreadyExists(self._config.bucket, exception)
            elif error_code == 'InvalidBucketName':
                raise SamsAmazonS3Errors.InvalidBucketName(self._config.bucket, exception)
            elif error_code == '404':
                raise SamsAssetErrors.AssetNotFound(kwargs.get('media_id'))

            logger.exception(exception)
            raise SamsAmazonS3Errors.UnknownAmazonException(exception)

        logger.exception(exception)
        raise

    def exists(self, media_id: str) -> bool:
        """Checks if a file exists in S3

        :params str media_id: The media_id from the Asset
        :return: ``True`` if a matching file exists, ``False`` otherwise
        :rtype: bool
        """

        try:
            self._client.head_object(
                Bucket=self._config.bucket,
                Key=self._get_key(media_id)
            )
            return True
        except Exception as ex:
            try:
                self._raise_amazon_exception(ex)
            except SamsAssetErrors.AssetNotFound:
                return False

    def put(self, content: Union[BinaryIO, bytes], filename: str, mimetype: str = None) -> str:
        """Upload a file to S3

        :param bytes content: The data to be uploaded
        :param str filename: The filename
        :param str mimetype: The mimetype of the content (not used here)
        :return: The ``"key"`` of the S3 object (excluding folder prefix)
        :rtype: str
        """

        try:
            _id = self._generate_key(filename, mimetype)
            self._client.upload_fileobj(
                content,
                self._config.bucket,
                self._get_key(_id)
            )
            return _id
        except Exception as ex:
            self._raise_amazon_exception(ex)

    def get(self, media_id: str) -> AmazonObjectWrapper:
        """Get Asset binary from S3

        :param str media_id: The media_id of the Asset
        :return: A file-like object providing a :meth:`read` method
        :rtype: AmazonObjectWrapper
        """

        try:
            obj = self._client.get_object(
                Bucket=self._config.bucket,
                Key=self._get_key(media_id)
            )

            if obj:
                return AmazonObjectWrapper(
                    obj,
                    media_id,
                    {}
                )
        except Exception as ex:
            self._raise_amazon_exception(ex, media_id=media_id)

        raise SamsAssetErrors.AssetNotFound(media_id)

    def delete(self, media_id: str):
        """Delete a file from S3

        :param str media_id: The media_id of the Asset
        """

        try:
            self._client.delete_object(
                Bucket=self._config.bucket,
                Key=self._get_key(media_id)
            )
        except Exception as ex:
            self._raise_amazon_exception(ex)

    def drop(self):
        """Deletes all assets from the S3 bucket/folder"""

        try:
            for keys in self.get_all_keys_in_batches():
                try:
                    self._client.delete_objects(
                        Bucket=self._config.bucket,
                        Delete={
                            'Objects': [{'Key': key} for key in keys]
                        }
                    )
                except Exception as ex:
                    self._raise_amazon_exception(ex)

            try:
                self._client.delete_bucket(
                    Bucket=self._config.bucket
                )
            except Exception as ex:
                self._raise_amazon_exception(ex)
        except SamsAmazonS3Errors.BucketNotFound:
            pass

    def get_all_keys_in_batches(self):
        """Returns all the keys for a bucket/folder"""

        next_marker = ''
        while True:
            kwargs = dict(
                Bucket=self._config.bucket,
                Marker=next_marker,
                MaxKeys=MAX_KEYS,
            )

            if self._config.folder:
                kwargs['Prefix'] = self._config.folder

            try:
                objects = self._client.list_objects(**kwargs)
            except Exception as ex:
                self._raise_amazon_exception(ex)

            if not objects or len(objects.get('Contents', [])) == 0:
                return

            keys = [
                obj['Key']
                for obj in objects.get('Contents')
            ]
            next_marker = keys[-1]
            yield keys

    def create_bucket(self):
        """Creates a new bucket in the S3 region

        The name of the bucket is from the ``STORAGE_DESTINATION`` entry for this provider
        """

        try:
            if self._config.region:
                self._client.create_bucket(
                    Bucket=self._config.bucket,
                    CreateBucketConfiguration={
                        'LocationConstraint': self._config.region
                    }
                )
            else:
                self._client.create_bucket(
                    Bucket=self._config.bucket,
                )
        except Exception as ex:
            self._raise_amazon_exception(ex)
