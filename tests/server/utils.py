from typing import Tuple
from sams.default_settings import MONGO_URI


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
