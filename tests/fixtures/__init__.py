from tests.server.utils import get_test_db_host

test_sets = [{
    'name': 'Test_Set',
    'state': 'draft',
    'description': 'Set used for testing purposes',
    'destination_name': 'internal',
    'destination_config': {'test': '123'}
}, {
    'name': 'Test_Set_2',
    'state': 'draft',
    'description': 'Set used for testing 2 purposes',
    'destination_name': 'internal',
    'destination_config': {'test': '123'}
}]

db_host = get_test_db_host()

STORAGE_DESTINATIONS = [
    'MongoGridFS,internal,mongodb://{}/tests_sams'.format(db_host),
    'MongoGridFS,during_draft,mongodb://{}/tests_sams'.format(db_host)
]

MONGO_STORAGE_PROVIDER = 'sams.storage.providers.mongo.MongoGridFSProvider'
