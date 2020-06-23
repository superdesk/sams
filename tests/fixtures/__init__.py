
test_sets = [{
    'name': 'Test_Set',
    'state': 'draft',
    'description': 'Set used for testing purposes',
    'destination_name': 'internal',
    'destination_config': {'test': '123'}
}]

STORAGE_DESTINATIONS = [
    'MongoGridFS,internal,mongodb://localhost/tests_sams',
    'MongoGridFS,during_draft,mongodb://localhost/tests_sams'
]

MONGO_STORAGE_PROVIDER = 'sams.storage.providers.mongo.MongoGridFSProvider'
