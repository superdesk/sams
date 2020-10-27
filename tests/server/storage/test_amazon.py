import pytest
from typing import Dict

from sams.storage.providers.amazon import AmazonS3Provider, AmazonS3Config
from sams_client.errors import SamsAmazonS3Errors
from tests.server.utils import get_test_db_host, get_test_storage_destinations, create_test_config

db_host = get_test_db_host()


def test_amazon_missing_config():
    # All config attributes
    AmazonS3Config(create_test_config(dict(
        access='minioadmin',
        secret='minioadmin',
        region='minio',
        bucket='test',
        endpoint='http://{}:9000'.format(db_host),
        folder='unit_tests'
    )))

    # Without optional attributes
    AmazonS3Config(create_test_config(dict(
        access='minioadmin',
        secret='minioadmin',
        region='minio',
        bucket='test',
    )))

    with pytest.raises(SamsAmazonS3Errors.MissingAmazonConfig) as error:
        AmazonS3Config(create_test_config(dict(
            secret='minioadmin',
            region='minio',
            bucket='test',
        )))

    assert error.value.description == 'Required Amazon config "access" missing'

    with pytest.raises(SamsAmazonS3Errors.MissingAmazonConfig) as error:
        AmazonS3Config(create_test_config(dict(
            access='minioadmin',
            region='minio',
            bucket='test',
        )))

    assert error.value.description == 'Required Amazon config "secret" missing'

    with pytest.raises(SamsAmazonS3Errors.MissingAmazonConfig) as error:
        AmazonS3Config(create_test_config(dict(
            access='minioadmin',
            secret='minioadmin',
            bucket='test',
        )))

    assert error.value.description == 'Required Amazon config "region" missing'

    with pytest.raises(SamsAmazonS3Errors.MissingAmazonConfig) as error:
        AmazonS3Config(create_test_config(dict(
            access='minioadmin',
            secret='minioadmin',
            region='minio',
        )))

    assert error.value.description == 'Required Amazon config "bucket" missing'

    with pytest.raises(SamsAmazonS3Errors.InvalidAmazonDestinationConfig):
        AmazonS3Config('foo,bar')


def test_invalid_endpoint():
    config = create_test_config(dict(
        access='minioadmin',
        secret='minioadmin',
        region='minio',
        bucket='test',
        endpoint='{}:9000'.format(db_host),
        folder='unit_tests'
    ))

    with pytest.raises(SamsAmazonS3Errors.InvalidAmazonEndpoint):
        AmazonS3Provider('AmazonS3,test,' + config)


def test_invalid_credentials():
    with pytest.raises(SamsAmazonS3Errors.InvalidAccessKeyId):
        AmazonS3Provider(
            'AmazonS3,test,' + create_test_config(dict(
                access='failedaccess',
                secret='minioadmin',
                region='minio',
                bucket='test',
                endpoint='http://{}:9000'.format(db_host),
                folder='unit_tests'
            ))
        ).get('test-file')

    with pytest.raises(SamsAmazonS3Errors.InvalidSecret):
        AmazonS3Provider(
            'AmazonS3,test,' + create_test_config(dict(
                access='minioadmin',
                secret='failedsecret',
                region='minio',
                bucket='test',
                endpoint='http://{}:9000'.format(db_host),
                folder='unit_tests'
            ))
        ).get('test-file')


def test_amazon_create_bucket():
    provider = AmazonS3Provider(get_test_storage_destinations(True)[0])
    provider._config.bucket = 'test-create-bucket'

    try:
        provider.create_bucket()

        with pytest.raises(SamsAmazonS3Errors.BucketAlreadyExists):
            provider.create_bucket()

        provider._config.bucket = 'test_invalid'
        with pytest.raises(SamsAmazonS3Errors.InvalidBucketName):
            provider.create_bucket()
    finally:
        provider._config.bucket = 'test-create-bucket'
        provider.drop()


def test_bucket_not_found():
    provider = AmazonS3Provider(get_test_storage_destinations(True)[0])
    provider._config.bucket = 'test-bucket-not-found'

    with pytest.raises(SamsAmazonS3Errors.BucketNotFound):
        provider.get('test-file')
