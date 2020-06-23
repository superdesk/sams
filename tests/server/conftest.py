from os import environ
from sys import path
from pathlib import Path
from pytest import fixture

from sams.factory import get_app
from sams.storage.providers import providers
from sams.storage.destinations import destinations

from tests.fixtures import STORAGE_DESTINATIONS

root = (Path(__file__).parent / '..').resolve()
path.insert(0, str(root))


def get_test_config():
    env_uri = environ.get('MONGO_URI', 'mongodb://sams/test')
    env_host = env_uri.rsplit('/', 1)[0]
    mongo_uri = '/'.join([env_host, 'tests_sams'])

    return {
        'MONGO_DBNAME': 'tests_sams',
        'MONGO_URI': mongo_uri,
        'ELASTICSEARCH_INDEX': 'tests_sams',
        'SERVER_NAME': 'localhost:5700',
        'DEBUG': True,
        'TESTING': True,
        'STORAGE_DESTINATION_1': STORAGE_DESTINATIONS[0],
        'STORAGE_DESTINATION_2': STORAGE_DESTINATIONS[1]
    }


def clean_databases(app):
    app.data.mongo.pymongo().cx.drop_database(app.config['MONGO_DBNAME'])
    indices = '%s*' % app.config['ELASTICSEARCH_INDEX']
    es = app.data.elastic.es
    es.indices.delete(indices, ignore=[404])
    with app.app_context():
        app.data.init_elastic(app)


def clean_storage_destinations():
    for destination in destinations.all().values():
        destination.provider_instance().drop()


@fixture
def app():
    return get_app(
        import_name='sams_test',
        config=get_test_config()
    )


@fixture
def client(app):
    return app.test_client()


@fixture
def init_app(app):
    with app.app_context():
        app.data.init_elastic(app)
        clean_databases(app)
        clean_storage_destinations()
        yield


@fixture(autouse=True)
def clean_storage_registrations():
    providers.clear()
