from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from akeyless import UpdateSecretVal

from ansible.plugins.loader import lookup_loader


from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def update_secret_lookup():
    return lookup_loader.get('update_static_secret_value')


class TestUpdateSecretValueLookup(object):

    def test_is_lookup_base(self, update_secret_lookup):
        assert issubclass(type(update_secret_lookup), AkeylessLookupBase)

    def test_input_putput(self, mock_api_client, update_secret_lookup, base_vars):
        opts = dict(
            token="t-123",
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
            last_version=5,
            keep_prev_version='true',
        )

        secret_name = "foo-bar"

        update_secret_lookup.run(
            terms=[secret_name],
            akeyless_api_url=base_vars['akeyless_api_url'],
            **opts
        )

        expected_input = UpdateSecretVal(
            name=secret_name,
            value=opts.get('value'),
            format=opts.get('format'),
            inject_url=opts.get('urls'),
            password=opts.get('password'),
            username=opts.get('username'),
            custom_field=opts.get('custom_fields'),
            token=opts.get('token'),
            uid_token=opts.get('uid_token'),
            key=opts.get('key'),
            last_version=5,
            multiline=opts.get('multiline'),
            keep_prev_version='true',
        )

        mock_api_client.update_secret_val.assert_called_once_with(expected_input)
