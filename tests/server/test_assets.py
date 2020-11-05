import pytest
from copy import deepcopy

from superdesk import get_resource_service, json
from eve.utils import ParsedRequest

from sams.assets import get_service as get_asset_service
from sams.sets import get_service as get_set_service
from sams_client.errors import SamsAssetErrors

from tests.fixtures import test_sets
from tests.server.utils import load_file


def add_set(doc):
    sets_service = get_set_service()

    set_id = sets_service.post([doc])[0]
    provider = sets_service.get_provider_instance(set_id)

    return set_id, provider


def test_asset_is_internal(init_app, client):
    # Make sure this service is for internal consumption only
    resp = client.get('/internal/assets')
    assert resp.status_code == 404

    # Make sure the service exists, otherwise a key exception will be raised here
    service = get_resource_service('assets')
    assert service.find({}).count() == 0


def test_asset_upload(init_app):
    asset_service = get_asset_service()
    set_id, provider = add_set(deepcopy(test_sets[0]))

    original_bytes, original_size = load_file('tests/fixtures/file_example-jpg.jpg')

    asset_id = asset_service.post([{
        'set_id': set_id,
        'filename': 'file_example-jpg.jpg',
        'name': 'Jpeg Example',
        'description': 'Jpeg file asset example',
        'binary': original_bytes,
    }])[0]

    asset = asset_service.get_by_id(asset_id)
    assert asset['length'] == original_size
    assert asset['mimetype'] == 'image/jpeg'
    assert provider.exists(asset['_media_id'])

    asset_binary = asset_service.download_binary(asset_id)
    assert asset_binary.length == original_size
    assert asset_binary.read() == original_bytes


def test_asset_patch(init_app):
    asset_service = get_asset_service()
    set_id, provider = add_set(deepcopy(test_sets[0]))

    original_bytes, _ = load_file('tests/fixtures/file_example-jpg.jpg')

    asset_id = asset_service.post([{
        'set_id': set_id,
        'filename': 'file_example-jpg.jpg',
        'name': 'Jpeg Example',
        'description': 'Jpeg file asset example',
        'binary': original_bytes,
    }])[0]

    asset = asset_service.get_by_id(asset_id)
    original_media_id = asset['_media_id']
    original_binary = asset_service.download_binary(asset_id)

    updated_bytes, _ = load_file('tests/fixtures/file_example-docx.docx')
    asset_service.patch(asset_id, {
        'filename': 'file_example-docx.docx',
        'binary': updated_bytes
    })

    asset = asset_service.get_by_id(asset_id)
    updated_media_id = asset['_media_id']
    updated_binary = asset_service.download_binary(asset_id)

    # Test that the asset has a new ``_media_id`` and ``binary``
    assert original_media_id != updated_media_id
    assert original_binary != updated_binary
    assert asset['mimetype'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    # Test that the original binary has been deleted
    assert not provider.exists(original_media_id)
    assert provider.exists(updated_media_id)


def test_delete(init_app):
    asset_service = get_asset_service()
    set_id, provider = add_set(deepcopy(test_sets[0]))

    original_bytes, _ = load_file('tests/fixtures/file_example-jpg.jpg')

    asset_id = asset_service.post([{
        'set_id': set_id,
        'filename': 'file_example-jpg.jpg',
        'name': 'Jpeg Example',
        'description': 'Jpeg file asset example',
        'binary': original_bytes,
    }])[0]

    asset = asset_service.get_by_id(asset_id)
    media_id = asset['_media_id']

    assert provider.exists(media_id)

    asset_service.delete_action({'_id': asset_id})
    assert not provider.exists(media_id)


def test_binary_undefined(init_app):
    asset_service = get_asset_service()
    set_id, provider = add_set(deepcopy(test_sets[0]))

    with pytest.raises(SamsAssetErrors.BinaryNotSupplied):
        asset_service.post([{
            'set_id': set_id,
            'filename': 'file_example-jpg.jpg',
            'name': 'Jpeg Example',
            'description': 'Jpeg file asset example',
        }])


def test_upload_using_stream(init_app):
    asset_service = get_asset_service()
    set_id, provider = add_set(deepcopy(test_sets[0]))

    with open('tests/fixtures/file_example-jpg.jpg', 'rb') as f:
        asset_id = asset_service.post([{
            'set_id': set_id,
            'filename': 'file_example',
            'name': 'Jpeg Example',
            'description': 'Jpeg file asset example',
            'binary': f,
        }])[0]

        f.seek(0)
        original_bytes = f.read()
        original_size = f.tell()

        asset = asset_service.get_by_id(asset_id)
        media_id = asset['_media_id']

        assert asset['length'] == original_size
        assert asset['mimetype'] == 'image/jpeg'
        assert provider.exists(media_id)

        asset_binary = asset_service.download_binary(asset_id)
        assert asset_binary.length == original_size
        assert asset_binary.read() == original_bytes


def test_search_elastic(init_app):
    asset_service = get_asset_service()
    set_1, _ = add_set(deepcopy(test_sets[0]))
    set_2, _ = add_set(deepcopy(test_sets[1]))

    with open('tests/fixtures/file_example-jpg.jpg', 'rb') as f:
        asset_service.post([{
            'set_id': set_1,
            'filename': 'file_example-1',
            'name': 'Jpeg Example 1',
            'description': 'Jpeg file asset example 1',
            'tags': [{'code': 'abg123', 'name': 'Alpha Beta Gamma 123'}],
            'binary': f,
        }, {
            'set_id': set_1,
            'filename': 'file_example-2',
            'name': 'Jpeg Example 2',
            'description': 'Jpeg file asset example 2',
            'tags': [{'code': 'dez456', 'name': 'Delta Epsilon Zeta 456'}],
            'binary': f,
        }, {
            'set_id': set_2,
            'filename': 'file_example-3',
            'name': 'Jpeg Example 3',
            'description': 'Jpeg file asset example 3',
            'tags': [
                {'code': 'abg123', 'name': 'Alpha Beta Gamma 123'},
                {'code': 'dez456', 'name': 'Delta Epsilon Zeta 456'}
            ],
            'binary': f,
        }, {
            'set_id': set_2,
            'filename': 'file_example-4',
            'name': 'Jpeg Example 4',
            'description': 'Jpeg file asset example 4',
            'tags': [],
            'binary': f,
        }])

    def _search(query):
        req = ParsedRequest()
        req.args = {'source': json.dumps({'query': {'bool': query}})}
        return asset_service.get(req=req, lookup=None)

    def _search_tags():
        query = {'must': {'term': {'tags.code': 'abg123'}}}
        filenames = [asset['filename'] for asset in _search(query)]
        assert len(filenames) == 2
        assert 'file_example-1' in filenames
        assert 'file_example-3' in filenames

        query = {'must_not': {'term': {'tags.code': 'abg123'}}}
        filenames = [asset['filename'] for asset in _search(query)]
        assert len(filenames) == 2
        assert 'file_example-2' in filenames
        assert 'file_example-4' in filenames

    def _search_filename_exact():
        """Search for exact filename"""
        query = {'must': {'term': {'filename.keyword': 'example'}}}
        assert _search(query).count() == 0

        query = {'must': {'term': {'filename.keyword': 'file_example-2'}}}
        assert _search(query).count() == 1

    def _search_filename_words():
        """Search using a partial filename"""
        query = {'must': {'term': {'filename': 'example'}}}
        assert _search(query).count() == 4

        query = {'must': {'query_string': {'query': 'filename:(file AND "example-1")'}}}
        assert _search(query).count() == 1

    def _search_name_exact():
        """Search for exact name"""
        query = {'must': {'term': {'name.keyword': 'Example'}}}
        assert _search(query).count() == 0

        query = {'must': {'term': {'name.keyword': 'Jpeg Example 2'}}}
        assert _search(query).count() == 1

    def _search_name_words():
        """Search using a partial name"""
        query = {'must': {'term': {'name': 'example'}}}
        assert _search(query).count() == 4

        query = {'must': {'query_string': {'query': 'name:(Jpeg AND "Example 2")'}}}
        assert _search(query).count() == 1

    def _search_set_id():
        query = {'must': {'term': {'set_id': str(set_1)}}}
        filenames = [asset['filename'] for asset in _search(query)]
        assert len(filenames) == 2
        assert 'file_example-1' in filenames
        assert 'file_example-2' in filenames

    def _search_combined():
        query = {
            'must': [
                {'term': {'set_id': str(set_1)}},
                {'term': {'tags.code': 'dez456'}},
                {'term': {'name': '2'}}
            ]
        }
        filenames = [asset['filename'] for asset in _search(query)]
        assert filenames == ['file_example-2']

    _search_tags()
    _search_filename_exact()
    _search_filename_words()
    _search_name_exact()
    _search_name_words()
    _search_set_id()
    _search_combined()
