import pytest

from sams.storage.providers.mongo import MongoGridFSProvider
from sams.errors import SuperdeskApiError


def test_mongo_upload(init_app, app):
    provider = MongoGridFSProvider(app.config.get('STORAGE_DESTINATION_1'))

    with open('tests/fixtures/file_example-jpg.jpg', 'rb') as f:
        original_bytes = f.read()
        original_size = f.tell()

    item_id = provider.put(original_bytes, 'file_example-jpg.jpg')

    assert provider.exists(item_id)
    item = provider.get(item_id)
    assert item.filename == 'file_example-jpg.jpg'
    assert item.length == original_size
    assert item.read() == original_bytes

    provider.delete(item_id)
    assert not provider.exists(item_id)
    with pytest.raises(SuperdeskApiError) as error:
        provider.get(item_id)

    assert error.value.status_code == 404

    provider.delete(item_id)


def test_drop(init_app, app):
    provider = MongoGridFSProvider(app.config.get('STORAGE_DESTINATION_1'))

    with open('tests/fixtures/file_example-jpg.jpg', 'rb') as f:
        jpeg_id = provider.put(f, 'file_example-jpg.jpg')

    with open('tests/fixtures/file_example-docx.docx', 'rb') as f:
        docx_id = provider.put(f, 'file_example-docx.docx')

    assert provider.exists(jpeg_id)
    assert provider.exists(docx_id)

    provider.drop()

    assert not provider.exists(jpeg_id)
    assert not provider.exists(docx_id)
