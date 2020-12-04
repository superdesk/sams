#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# This file is part of SAMS.
#
# Copyright 2020 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from io import BytesIO
from behave import *
from flask import json
import hashlib
from werkzeug.http import unquote_etag
from zipfile import ZipFile

from tests.features.steps.helpers import assert_200, apply_placeholders, test_json, store_last_item, expect_status, \
    get_client_model_and_method_from_step
from tests.features.steps.apps.api import get_api, get_api_client
from tests.features.steps.apps.file_server import get_file_server_client


@when('we send client.{model_name}.{method_name}')
def step_impl_send_client(context, model_name, method_name):
    client, model, method = get_client_model_and_method_from_step(
        context,
        model_name,
        method_name
    )

    kwargs = {} if not context.text else json.loads(apply_placeholders(context, context.text))
    external_user_id = kwargs.pop('external_user_id', None)
    if external_user_id:
        context.response = method(external_user_id=external_user_id, **kwargs)
    else:
        context.response = method(**kwargs)

    store_last_item(context, model_name)


@when('we upload a binary file with client.{model_name}.{method_name}')
def step_impl_upload_binary_client(context, model_name, method_name):
    client, model, method = get_client_model_and_method_from_step(
        context,
        model_name,
        method_name
    )

    kwargs = {} if not context.text else json.loads(apply_placeholders(context, context.text))
    filename = kwargs.pop('filename', None)
    external_user_id = kwargs.pop('external_user_id', None)
    filepath = None if not filename else 'tests/fixtures/{}'.format(filename)
    files = None if not filepath else {'binary': open(filepath, 'rb')}

    if external_user_id:
        context.response = method(files=files, external_user_id=external_user_id, **kwargs)
    else:
        context.response = method(files=files, **kwargs)
    store_last_item(context, model_name)


@when('we download a binary file with client.{model_name}.{method_name}')
def step_impl_download_binary_client(context, model_name, method_name):
    client, model, method = get_client_model_and_method_from_step(
        context,
        model_name,
        method_name
    )

    kwargs = {} if not context.text else json.loads(apply_placeholders(context, context.text))
    context.response = method(**kwargs)


@when('we get "{url}"')
def step_impl_get(context, url: str):
    url = apply_placeholders(context, url)

    context.response = get_api_client(context).get(url=url)


@when('we download from the file server /assets/{url}')
def step_impl_get_from_public(context, url):
    url = '/assets/' + apply_placeholders(context, url)

    context.response = get_file_server_client(context).get(url=url)


@then('we get file response with headers')
def step_impl_get_file_response_with_headers(context):
    assert_200(context.response)

    data = {} if not context.text else json.loads(apply_placeholders(context, context.text))

    for key, value in data.items():
        header_value = context.response.headers[key]
        if isinstance(value, int):
            header_value = int(header_value)

        assert value == header_value, 'response.{}({}) != expected.{}({})'.format(
            key,
            header_value,
            key,
            value
        )

    response_etag, _ = unquote_etag(context.response.headers['ETag'])
    h = hashlib.sha1()
    h.update(context.response.content)
    expected_etag = h.hexdigest()

    assert response_etag == expected_etag, 'response.etag({}) != expected.etag({})'.format(
        response_etag,
        expected_etag
    )

    if data.get('Content-Length'):
        content_size = len(context.response.content)
        assert content_size == data['Content-Length'], 'response.length({}) != expected.length({})'.format(
            content_size,
            data['Content-Length']
        )


@then('we get zip file with assets')
def step_impl_and_we_get_zip_file_with_assets(context):
    zip_file = ZipFile(BytesIO(context.response.content))
    assert zip_file.testzip() is None

    data = {} if not context.text else json.loads(apply_placeholders(context, context.text))
    item_ids = data['item_ids']
    assets = get_api_client(context).assets.get_by_ids(item_ids).json()['_items']

    zip_filenames = zip_file.namelist()
    for asset in assets:
        assert asset['filename'] in zip_filenames


@when('we post "{url}"')
def step_impl_post(context, url: str):
    url = apply_placeholders(context, url)
    data = None if not context.text else json.loads(apply_placeholders(context, context.text))

    context.response = get_api_client(context).post(
        url=url,
        data=data
    )


@when('we patch "{url}"')
def step_impl_post(context, url: str):
    url = apply_placeholders(context, url)
    data = None if not context.text else json.loads(apply_placeholders(context, context.text))

    context.response = get_api_client(context).patch(
        url=url,
        data=data
    )


@when('we delete "{url}"')
def step_impl_post(context, url: str):
    url = apply_placeholders(context, url)

    context.response = get_api_client(context).delete(url=url)


@then('we get OK response')
def step_impl_then_get_ok(context):
    assert_200(context.response)


@then('we get response code {code}')
def step_impl_then_get_code(context, code):
    assert context.response.status_code == int(code)


@then('we get error {code}')
def step_impl_then_get_error(context, code):
    expect_status(context.response, int(code))
    if context.text:
        test_json(context)


@then('we get existing resource')
def step_impl_then_get_existing(context):
    if not isinstance(context.response, tuple):
        assert_200(context.response)
    test_json(context)


@given('server config')
def step_impl_server_config(context):
    api = get_api(context)
    config = json.loads(apply_placeholders(context, context.text))
    api.init(config)
    api.start()
    context.app_api = api
    context._reset_after_scenario = True


@given('client config')
def step_impl_client_config(context):
    app = get_api(context)
    config_overrides = json.loads(
        apply_placeholders(context, context.text)
    )
    app.client = app.create_client_instance(config_overrides)


@then('we store response in "{tag}"')
def step_impl_store_response_in_cts(context, tag):
    data = json.loads(context.response.content)
    setattr(context, tag, data)
