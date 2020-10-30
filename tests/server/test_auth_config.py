from sams.apps.api.app import get_app
from sams.auth.public import PublicAuth
from tests.server.mock_auth_reject import MockAuthReject


def test_default_auth():
    app = get_app(config={'SAMS_AUTH_TYPE': 'sams.auth.public'})

    assert 'SAMS_AUTH_TYPE' in app.config
    assert app.config['SAMS_AUTH_TYPE'] == 'sams.auth.public'
    assert isinstance(app.auth, PublicAuth)

    resp = app.test_client().get('/')
    assert resp.status_code == 200


def test_custom_auth():
    app = get_app(config={'SAMS_AUTH_TYPE': 'tests.server.mock_auth_reject'})

    assert 'SAMS_AUTH_TYPE' in app.config
    assert app.config['SAMS_AUTH_TYPE'] == 'tests.server.mock_auth_reject'
    assert isinstance(app.auth, MockAuthReject)

    resp = app.test_client().get('/')
    assert resp.status_code == 401
