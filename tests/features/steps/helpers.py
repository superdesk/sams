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

from wooper.expect import expect_status_in, fail_and_print_body
from wooper.assertions import assert_equal
from datetime import datetime, timedelta
import arrow
from re import findall

from requests.models import Response
from flask import json

from superdesk.utc import utcnow
from tests.features.steps.apps.api import get_api_client

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def assert_200(response: Response):
    """Assert we get status code 200."""
    expect_status_in(response, [200, 201, 204])


def assert_404(response: Response):
    """Assert we get status code 404."""
    assert response.status_code == 404, 'Expected 404, got {}'.format(response.status_code)


def test_key_is_present(key, context, response):
    """Test if given key is present in response.

    In case the context value is empty - "", {}, [] - it checks if it's non empty in response.

    If it's set in context to false, it will check that it's falsy/empty in response too.

    :param key
    :param context
    :param response
    """
    assert not isinstance(context[key], bool) or not response[key], \
        '"%s" should be empty or false, but it was "%s" in (%s)' % (key, response[key], response)


def test_key_is_not_present(key, response):
    """Test if given key is not present in response.

    :param key
    :param response
    """
    assert key not in response, \
        '"%s" should not be present, but it was "%s" in (%s)' % (key, response[key], response)


def assert_is_now(val, key):
    """Assert that given datetime value is now (with 2s tolerance).

    :param val: datetime
    :param key: val label - used for error reporting
    """
    now = arrow.get()
    val = arrow.get(val)
    assert val + timedelta(seconds=5) > now, '%s should be %s, it is %s' % (key, now, val)


def format_date(date_to_format):
    return date_to_format.strftime(DATETIME_FORMAT)


def apply_placeholders(context, text):
    placeholders = getattr(context, 'placeholders', {})
    for placeholder in findall('#([^#"]+)#', text):
        if placeholder.startswith('DATE'):
            value = utcnow()
            unit = placeholder.find('+')
            if unit != -1:
                value += timedelta(days=int(placeholder[unit + 1]))
            else:
                unit = placeholder.find('-')
                if unit != -1:
                    value -= timedelta(days=int(placeholder[unit + 1]))

            value = format_date(value)
            placeholders['LAST_DATE_VALUE'] = value
        elif placeholder not in placeholders:
            try:
                resource_name, field_name = placeholder.split('.', maxsplit=1)
            except Exception:
                continue
            resource = getattr(context, resource_name, None)
            for name in field_name.split('.'):
                if not resource:
                    break

                resource = resource.get(name, None)

            if not resource:
                continue

            if isinstance(resource, datetime):
                value = format_date(resource)
            else:
                value = str(resource)
        else:
            value = placeholders[placeholder]
        text = text.replace('#%s#' % placeholder, value)
    return text


def json_match(context_data, response_data, json_fields=None):
    if json_fields is None:
        json_fields = []

    if isinstance(context_data, dict):
        if (not isinstance(response_data, dict)):
            return False
        for key in context_data:
            if context_data[key] == "__none__":
                assert response_data.get(key) is None, '{} is not None ({})'.format(key, response_data[key])
                continue
            if context_data[key] == "__no_value__":
                test_key_is_not_present(key, response_data)
                continue
            if key not in response_data:
                print(key, ' not in ', response_data)
                return False
            if context_data[key] == "__any_value__":
                test_key_is_present(key, context_data, response_data)
                continue
            if context_data[key] == "__now__":
                assert_is_now(response_data[key], key)
                continue
            if context_data[key] == "__empty__":
                assert len(response_data[key]) == 0, '%s is not empty (%s)' % (key, response_data[key])
                continue
            response_field = response_data[key]
            if key in json_fields:
                try:
                    response_field = json.loads(response_data[key])
                except Exception:
                    fail_and_print_body(response_data,
                                        'response does not contain a valid %s field' % key)
            if not json_match(context_data[key], response_field, json_fields):
                return False
        return True
    elif isinstance(context_data, list):
        for item_context in context_data:
            found = False
            for item_response in response_data:
                if json_match(item_context, item_response, json_fields):
                    found = True
                    break
            if not found:
                print(item_context, ' not in ', json.dumps(response_data, indent=2))
                return False
        return True
    elif not isinstance(context_data, dict):
        if context_data != response_data:
            print('---' + str(context_data) + '---\n', ' != \n', '---' + str(response_data) + '---\n')
        return context_data == response_data


def test_json(context, json_fields=None):
    if json_fields is None:
        json_fields = []

    if isinstance(context.response, tuple):
        response_data = context.response[0]
    else:
        try:
            response_data = json.loads(context.response.text)
        except Exception:
            fail_and_print_body(context.response, 'response is not valid json')
            return

        try:
            context_data = json.loads(context.text)
        except Exception:
            fail_and_print_body(context, 'response is not valid json')
            return

    context_data = json.loads(
        apply_placeholders(
            context,
            context.text
        )
    )
    assert_equal(
        json_match(context_data, response_data, json_fields),
        True,
        msg=str(context_data) + '\n != \n' + str(response_data)
    )

    return response_data


def store_last_item(context, model_name: str):
    if isinstance(context.response, tuple):
        if not context.response[1] in (200, 201):
            return
        item = context.response[0]
        try:
            setattr(context, model_name.upper(), item)
        except (IndexError, KeyError):
            pass
    else:
        if not context.response.status_code in (200, 201):
            return
        try:
            item = json.loads(context.response.text)
        except ValueError:
            assert False, context.response.text
        if item.get('_status') == 'OK' and item.get('_id'):
            try:
                setattr(context, model_name.upper(), item)
            except (IndexError, KeyError):
                pass


def expect_status(response, code):
    assert int(code) == response.status_code, 'expected {expected}, got {code}, reason={reason}'.format(
        code=response.status_code,
        expected=code,
        reason=response.text,
    )


def get_client_model_and_method_from_step(context, model_name, method_name):
    client = get_api_client(context)

    try:
        model = getattr(client, model_name)
    except AttributeError:
        assert False, 'client.{} is not registered with the client'.format(model_name)

    try:
        method = getattr(model, method_name)
    except AttributeError:
        assert False, 'client.{}.{} is not registered with the client'.format(model_name, method_name)

    return client, model, method
