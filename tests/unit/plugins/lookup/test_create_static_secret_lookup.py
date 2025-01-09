from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from akeyless import CreateSecret

from ansible.plugins.loader import lookup_loader



from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def create_secret_lookup():
    return lookup_loader.get('create_static_secret')


class TestCreateStaticSecretLookup(object):

    def test_is_lookup_base(self, create_secret_lookup):
        assert issubclass(type(create_secret_lookup), AkeylessLookupBase)

    def test_input_output(self, mock_api_client, create_secret_lookup, base_vars):
        opts = dict(
            token="t-123",
            description="a great item",
            type="generic",
            value="a value",
            format="json",
            urls=["a", "b"],
            password="some-pass",
            username="dani",
            custom_fields=["x", "y", "z"],
            tags=["aaa"],
            key="key1",
            uid_token="uid-123",
            multiline=True,
        )

        secret_name = "foo-bar"

        create_secret_lookup.run(
            terms=[secret_name],
            akeyless_api_url=base_vars['akeyless_api_url'],
            **opts
        )

        expected_create_secret = CreateSecret(
            name=secret_name,
            description=opts.get('description'),
            type=opts.get('type'),
            value=opts.get('value'),
            format=opts.get('format'),
            inject_url=opts.get('urls'),
            password=opts.get('password'),
            username=opts.get('username'),
            custom_field=opts.get('custom_fields'),
            tags=opts.get('tags'),
            token=opts.get('token'),
            protection_key=opts.get('key'),
            multiline_value=opts.get('multiline'),
            uid_token=opts.get('uid_token'),
        )

        mock_api_client.create_secret.assert_called_once_with(expected_create_secret)
