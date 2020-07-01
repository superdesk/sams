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

from behave import *
from flask import json

from tests.features.steps.helpers import assert_200, apply_placeholders, test_json, store_last_item, expect_status
from tests.features.steps.app import get_app, get_client


@when('we send client.{model_name}.{method_name}')
def step_impl_send_client(context, model_name, method_name):
    client = get_client(context)

    try:
        model = getattr(client, model_name)
    except AttributeError:
        assert False, 'client.{} is not registered with the client'.format(model_name)

    try:
        method = getattr(model, method_name)
    except AttributeError:
        assert False, 'client.{}.{} is not registered with the client'.format(model_name, method_name)

    kwargs = {} if not context.text else json.loads(apply_placeholders(context, context.text))
    context.response = method(**kwargs)
    store_last_item(context, model_name)


@when('we get "{url}"')
def step_impl_get(context, url: str):
    url = apply_placeholders(context, url)

    context.response = get_client(context).get(url=url)


@when('we post "{url}"')
def step_impl_post(context, url: str):
    url = apply_placeholders(context, url)
    data = None if not context.text else json.loads(apply_placeholders(context, context.text))

    context.response = get_client(context).post(
        url=url,
        data=data
    )


@when('we patch "{url}"')
def step_impl_post(context, url: str):
    url = apply_placeholders(context, url)
    data = None if not context.text else json.loads(apply_placeholders(context, context.text))

    context.response = get_client(context).patch(
        url=url,
        data=data
    )


@when('we delete "{url}"')
def step_impl_post(context, url: str):
    url = apply_placeholders(context, url)

    context.response = get_client(context).delete(url=url)


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
    assert_200(context.response)
    test_json(context)


@given('app config')
def step_impl_app_config(context):
    app = get_app(context)
    config = json.loads(apply_placeholders(context, context.text))
    app.init(config)
    app.start()
    context.app = app
