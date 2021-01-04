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

from bson import ObjectId
from typing import Dict, List, Tuple, Any, Union

try:
    # When used in the SAMS API errors will inherit from Werkzeug errors
    # to ensure Eve Validation errors are passed through here
    from werkzeug.exceptions import HTTPException, BadRequest as BaseException
except ImportError:
    # Otherwise when used in the SAMS Client, normal Exception errors will do
    HTTPException = Any
    BaseException = Exception


try:
    from flask import current_app as app
except ImportError:
    app = {'config': {}}

from sams_client.utils import bytes_to_human_readable


class SamsException(BaseException):
    """Base class used for all SAMS Errors

    :var str app_code: The unique SAMS code for this error
    :var int http_code: The HTTP status code to send to the client
    :var str description: The description of the error
    :var bool log_exception: If ``True``, the stack trace will be logged
    """

    app_code: str = '01001'
    http_code: int = 500
    description: str = ''
    log_exception: bool = False

    def __init__(self, payload: Dict[str, Any] = None, exception: Exception = None):
        super().__init__()
        self.payload = payload or {}
        self.exception = exception
        self.description = self.description.format(**self.payload)

    def get_name(self) -> str:
        """Returns the class name of the exception.
        For example::

            SamsSetErrors.InvalidStateTransition('usable').get_name()
            'InvalidStateTransition'
        """

        return self.__class__.__name__

    def __str__(self) -> str:
        """Returns a string containing all relevant information
        For example::

            str(SamsSetErrors.InvalidStateTransition('usable'))
            'Error[07001] - InvalidStateTransition: Cannot change state from "usable" to draft'
        """

        return 'Error[{}] - {}: {}'.format(
            self.app_code,
            self.get_name(),
            self.description
        )

    def to_dict(self) -> Dict[str, str or Dict]:
        """Returns a dictionary with all the relevant information

        This is used for constructing the response to send to the client.
        For example::

            SamsSetErrors.InvalidStateTransition('usable').to_dict()
            {
                'error': '07001',
                'name': 'InvalidStateTransition',
                'description': 'Cannot change state from "usable" to draft'
            }
        """

        return {
            'error': self.app_code,
            'name': self.get_name(),
            'description': self.description,
        }

    def to_error_response(self) -> Tuple[Union[Dict[str, str or Dict], str], int]:
        """Returns a tuple containing a results of ``to_dict()`` and ``http_code``
        For example::

            SamsSetErrors.InvalidStateTransition('usable').to_error_response()
            {
                'error': '07001',
                'name': 'InvalidStateTransition',
                'description': 'Cannot change state from "usable" to draft'
            },
            400
        """

        if (getattr(app, 'config') or {}).get('RETURN_ERRORS_AS_JSON', False):
            return self.to_dict(), self.http_code
        else:
            return str(self), self.http_code


class SamsSystemErrors:
    class UnknownError(SamsException):
        """Raised when an unknown/unhandled error has occurred"""

        app_code = '01001'
        http_code = 500
        description = '{message}'
        log_exception = True

        def __init__(self, message: str, exception: Exception = None):
            super().__init__({'message': str(message)}, exception)

    class AssertionError(UnknownError):
        """Raised when an assertion has failed in the code"""

        app_code = '01002'
        http_code = 500
        description = '{message}'
        log_exception = True

    class SystemUpdateNotAllowed(SamsException):
        """Raised when an attempt to force resource update from an API endpoint"""

        app_code = '01003'
        http_code = 500
        description = '"system_update" not allowed in api endpoints'
        log_exception = True

    class NotImplemented(UnknownError):
        """Raised when a required function has not been implemented"""

        app_code = '01004'
        http_code = 500
        description = '{message}'
        log_exception = True


class SamsConfigErrors:
    class AuthTypeNotSpecified(SamsException):
        """Raised when the `SAMS_AUTH_TYPE` config attribute is undefined"""

        app_code = '02001'
        http_code = 500
        description = 'Auth type not specified'
        log_exception = True

    class AuthTypeHasNoGetAuthInstance(SamsException):
        """Raised when loading the Auth module if `get_auth_instance` is undefined"""

        app_code = '02002'
        http_code = 500
        description = 'Configured Auth type must have a "get_auth_instance" method'
        log_exception = True

    class StorageProviderConfigStringNotProvided(SamsException):
        """Raised when a StorageProvider receives an empty config"""

        app_code = '02003'
        http_code = 500
        description = '"config_string" must be provided'
        log_exception = True

    class StorageProviderIncorrectConfigArguments(SamsException):
        """Raised when a StorageProvider received incorrect number of config arguments"""

        app_code = '02004'
        http_code = 500
        description = 'Incorrect number of arguments, expected 3 but received {num_args}'
        log_exception = True

        def __init__(self, num_args: int, exception: Exception = None):
            super().__init__({'num_args': num_args}, exception)

    class StorageProviderInvalidConfig(SamsException):
        """Raised when a StorageProvider received config for an incompatible StorageProvider"""

        app_code = '02005'
        http_code = 500
        description = 'Incorrect config entry for provider {dest_provider}, received entry for {src_provider}'
        log_exception = True

        def __init__(self, src_provider: str, dest_provider: str, exception: Exception = None):
            super().__init__({'src_provider': src_provider, 'dest_provider': dest_provider}, exception)

    class BasicAuthAPIKeysNotProvided(SamsException):
        """Raised when `sams.auth.basic` authentication is used without any API keys defined"""

        app_code = '02006'
        http_code = 501
        description = 'No API keys defined in the config'
        log_exception = True


class SamsHTTPError(SamsException):
    """All generic HTTP errors will be raised with this error.

    The ``app_code`` will be the supplied ``http_code`` prefixed with ``03``.
    For example::

        from flask import abort

        abort(401, description='Not allowed to do that')

        # will raise the following error
        {
            "error": "03401",
            "name": "SamsHTTPError",
            "description": "Not allowed to do that"
        }

    This method solely exists to catch errors that are raised from underlying frameworks, such as ``Eve`` or ``Flask``

    It is advised not to use ``abort`` directly, instead implement a new exception that extends the ``SamsException``
    class.
    """

    app_code = '03'

    def __init__(self, error: HTTPException):
        self.error = error
        self.http_code = error.code
        self.app_code = '{}{}'.format(
            self.app_code,
            self.http_code
        )
        self.description = error.description

    def get_name(self) -> str:
        return self.error.name


class SamsResourceErrors:
    class ValidationError(SamsException):
        """Raised when receiving an invalid request to create or update a resource

        The response will include the list of fields and rules that failed validation, under the ``errors`` attribute.
        For example::

            "error": "04001",
            "name": "ValidationError",
            "description": "Validation error",
            "errors": {
                "name": ["required"]
            }

        This indicates that the field ``name`` was not supplied with the request (or was ``null``).
        """

        app_code = '04001'
        http_code = 400
        description = 'Validation error'
        errors: Dict[str, List[str]] = {}

        def __init__(self, errors: Dict[str, str or Dict[str, Any]]):
            super().__init__()

            self.errors = {}
            for field, errors in errors.items():
                if isinstance(errors, str):
                    self.errors[field] = [errors]
                elif isinstance(errors, dict):
                    self.errors[field] = list(errors.keys())

        def to_dict(self) -> Dict[str, str or List[str]]:
            data = super().to_dict()
            data['errors'] = self.errors
            return data

    class InvalidSearchQuery(SamsException):
        """Raised when an invalid ElasticSearch query was received"""

        app_code = '04002'
        http_code = 400
        description = 'Invalid search query'
        log_exception = True

    class AuthNotSupplied(SamsException):
        """Raised when authentication failed"""

        app_code = '04003'
        http_code = 401
        description = 'Please provide proper credentials'


class SamsStorageDestinationErrors:
    class NotFound(SamsException):
        """Raised when the ``StorageDestination`` could not be found"""

        app_code = '05001'
        http_code = 404
        description = 'Destination "{destination_id}" not registered with the system'

        def __init__(self, destination_id: str, exception: Exception = None):
            super().__init__({'destination_id': destination_id}, exception)


class SamsStorageProviderErrors:
    class NotFound(SamsException):
        """Raised when the ``StorageProvider`` could not be found"""

        app_code = '06001'
        http_code = 404
        description = 'Provider "{provider_id}" not registered with the system'

        def __init__(self, provider_id: str, exception: Exception = None):
            super().__init__({'provider_id': provider_id}, exception)


class SamsSetErrors:
    class InvalidStateTransition(SamsException):
        """Raised when attempting to convert an active Set back to ``draft``"""

        app_code = '07001'
        http_code = 400
        description = 'Cannot change state from "{state}" to draft'

        def __init__(self, state: str, exception: Exception = None):
            super().__init__({'state': state}, exception)

    class DestinationChangeNotAllowed(SamsException):
        """Raised when attempting to change the ``StorageDestination`` of an active Set"""

        app_code = '07002'
        http_code = 400
        description = 'Destination can only be changed in draft state'

    class DestinationConfigChangeNotAllowed(SamsException):
        """Raised when attempting to change the ``StorageDestination`` config of an active Set"""

        app_code = '07003'
        http_code = 400
        description = 'Destination config can only be changed in draft state'

    class DestinationNotFound(SamsException):
        """Raised when the ``StorageDestination`` could not be found"""

        app_code = '07004'
        http_code = 400
        description = 'Destination "{destination_id}" isnt configured'

        def __init__(self, destination_id: str, exception: Exception = None):
            super().__init__({'destination_id': destination_id}, exception)

    class CannotDeleteActiveSet(SamsException):
        """Raised when attempting to delete an active Set or Inactive Set with Assets"""

        app_code = '07005'
        http_code = 400
        description = 'Can only delete Sets that are in draft state or disabled with no assets'

    class SetNotFound(SamsException):
        """Raised when a Set cannot be found"""

        app_code = '07006'
        http_code = 400
        description = 'Set with id {set_id} not found'

        def __init__(self, set_id: ObjectId, exception: Exception = None):
            super().__init__({'set_id': str(set_id)}, exception)


class SamsAssetErrors:
    class BinaryNotSupplied(SamsException):
        """Raised when attempting to create a new Asset without an associated binary data"""

        app_code = '08001'
        http_code = 400
        description = 'Asset must contain a binary to upload'

    class AssetNotFound(SamsException):
        """Raised when attempting to download the binary of a non-existent Asset"""

        app_code = '08002'
        http_code = 404
        description = 'Asset with id "{asset_id}" not found'

        def __init__(self, asset_id: Union[ObjectId, str], exception: Exception = None):
            super().__init__({'asset_id': str(asset_id)}, exception)

    class AssetUploadToInactiveSet(SamsException):
        """Raised when attempting to create a new Asset into an inactive set"""

        app_code = '08003'
        http_code = 400
        description = 'Asset upload is not allowed to an inactive Set'

    class AssetExceedsMaximumSizeForSet(SamsException):
        """Raised when an Asset size exceeds the configured max size of a Set"""

        app_code = '08004'
        http_code = 400
        description = 'Asset size ({asset_size}) exceeds the maximum size for the Set ({max_size})'

        def __init__(self, asset_size: int, max_size: int):
            super().__init__({
                'asset_size': bytes_to_human_readable(asset_size),
                'max_size': bytes_to_human_readable(max_size),
            })

    class ExternalUserIdNotFound(SamsException):
        """Raised when attempting to create/update Asset without External User Id"""

        app_code = '08005'
        http_code = 400
        description = 'External User ID not found'

    class ExternalSessionIdNotFound(SamsException):
        """Raised when attempting to create/update Asset without External Session Id"""

        app_code = '08006'
        http_code = 400
        description = 'External Session ID not found'

    class ExternalUserIdDoNotMatch(SamsException):
        """Raised when attempting to create/update Asset with different External User Id"""

        app_code = '08007'
        http_code = 400
        description = 'External User ID does not match'

    class ExternalSessionIdDoNotMatch(SamsException):
        """Raised when attempting to create/update Asset with different External Session Id"""

        app_code = '08008'
        http_code = 400
        description = 'External Session ID does not match'

    class LockingAssetLocked(SamsException):
        """Raised when attempting to lock an already locked asset"""

        app_code = '08009'
        http_code = 400
        description = 'Can not Lock asset which is already locked'

    class UnlockingAssetUnlocked(SamsException):
        """Raised when attempting to unlock an already unlocked asset"""

        app_code = '08010'
        http_code = 400
        description = 'Can not Unlock asset which is already unlocked'


class SamsAmazonS3Errors:
    class InvalidAmazonEndpoint(SamsException):
        """Raised when an invalid config is provided"""

        app_code = '09001'
        http_code = 500
        description = 'Invalid Amazon URL'

    class InvalidAccessKeyId(SamsException):
        """Raised when an invalid access key id was provided"""

        app_code = '09002'
        http_code = 500
        description = 'Invalid AccessKeyId provided'

    class InvalidSecret(SamsException):
        """Raised when an invalid access key id was provided"""

        app_code = '09003'
        http_code = 500
        description = 'Invalid Secret provided'

    class MissingAmazonConfig(SamsException):
        """Raised when the config is missing a required field"""

        app_code = '09004'
        http_code = 500
        description = 'Required Amazon config "{key}" missing'

        def __init__(self, key: str, exception: Exception = None):
            super().__init__({'key': key}, exception)

    class InvalidAmazonDestinationConfig(SamsException):
        """Raised when Amazon destination config string was provided"""

        app_code = '09005'
        http_code = 500
        description = 'Invalid Amazon destination config "{config}". Error: {error}'

        def __init__(self, config: str, exception: Exception = None):
            super().__init__({'config': config, 'error': str(exception)}, exception)

    class BucketNotFound(SamsException):
        """Raised when the configured bucket does not exist"""

        app_code = '09006'
        http_code = 500
        description = 'Amazon bucket "{bucket}" not found'

        def __init__(self, bucket: str, exception: Exception = None):
            super().__init__({'bucket': bucket}, exception)

    class BucketAlreadyExists(SamsException):
        """Raised when attempting to create a bucket that already exists"""

        app_code = '09007'
        http_code = 400
        description = 'Amazon bucket "{bucket}" already exists'

        def __init__(self, bucket: str, exception: Exception = None):
            super().__init__({'bucket': bucket}, exception)

    class InvalidBucketName(SamsException):
        """Raised when using an invalid AWS Bucket name"""

        app_code = '09008'
        http_code = 500
        description = 'Invalid Amazon bucket name "{bucket}"'

        def __init__(self, bucket: str, exception: Exception = None):
            super().__init__({'bucket': bucket}, exception)

    class UnknownAmazonException(SamsException):
        """Raised when an unknown Amazon error was raised"""

        app_code = '09999'
        http_code = 500
        description = 'Unknown Amazon error: {error}'

        def __init__(self, exception: Exception):
            super().__init__({'error': str(exception)}, exception)
