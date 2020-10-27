from typing import Tuple, Dict
from sams.default_settings import MONGO_URI, env, strtobool


def dict_contains(object: dict, tests: dict):
    for key, value in tests.items():
        if object.get(key) != value:
            return False

    return True


def load_file(filename: str) -> Tuple[bytes, int]:
    with open(filename, 'rb') as f:
        data = f.read()
        size = f.tell()

        return data, size


def get_test_db_host() -> str:
    return MONGO_URI.rsplit('/', 1)[0].replace('mongodb://', '')


def create_test_config(attributes: Dict[str, str]):
    return ','.join([
        '{}={}'.format(key, val)
        for key, val in attributes.items()
    ])


def get_test_storage_destinations(force_test_s3: bool = False):
    db_host = get_test_db_host()

    if force_test_s3 or strtobool(env('TEST_AMAZON_S3', 'false')):
        return [
            'AmazonS3,internal,' + create_test_config(dict(
                access='minioadmin',
                secret='minioadmin',
                region='minio',
                bucket='test',
                endpoint='http://{}:9000'.format(db_host),
            )),
            'AmazonS3,during_draft,' + create_test_config(dict(
                access='minioadmin',
                secret='minioadmin',
                region='minio',
                bucket='test',
                endpoint='http://{}:9000'.format(db_host),
                folder='media_files'
            ))
        ]
    else:
        return [
            'MongoGridFS,internal,mongodb://{}/tests_sams'.format(db_host),
            'MongoGridFS,during_draft,mongodb://{}/tests_sams'.format(db_host)
        ]
