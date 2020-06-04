from flask import json


def test_bootstrap_app(init_app, client):
    resp = client.get('/')
    assert resp.status_code == 200
    data = json.loads(resp.get_data())

    assert '_links' in data
    assert 'child' in data['_links']

    # {'_links': {'child': []}}
    # from pprint import pprint
    # pprint(data)
    # assert 1 == 2
