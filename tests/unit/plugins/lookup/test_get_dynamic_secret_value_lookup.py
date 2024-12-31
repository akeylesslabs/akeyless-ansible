from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import  GetDynamicSecretValue

from ansible.plugins.loader import lookup_loader

from unittest import mock

from plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def get_ds_value_lookup():
    return lookup_loader.get('get_dynamic_secret_value')


@pytest.fixture(params=["get_ds_value_response.json"])
def get_ds_value_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetDynamicSecretValueLookup(object):

    def test_is_lookup_base(self, get_ds_value_lookup):
        assert issubclass(type(get_ds_value_lookup), AkeylessLookupBase)


    def test_raise_error(self, mock_api_client, get_ds_value_lookup, base_vars):
        get_ds_value_lookup.authenticate = mock.Mock(return_value=mock.Mock(token="t-123abc"))

        mock_api_client.get_dynamic_secret_value.side_effect = Exception("Somthing is not working")

        with pytest.raises(Exception, match="Unknown exception trying to run get_dynamic_secret_value"):
            get_ds_value_lookup.run(terms=["a great ds"], akeyless_url=base_vars['akeyless_url'])


    def test_input_output(self, mock_api_client, get_ds_value_lookup, get_ds_value_response, base_vars):
        mock_api_client.get_dynamic_secret_value.return_value = get_ds_value_response.copy()

        opts = dict(
            token="t-123",
            host="localhost:2312",
            timeout=15,
            path="/x/y",
            args=["a=b", "c=d"]
        )
        ds_name = "fake-mysql-ds"
        response = get_ds_value_lookup.run(
            terms=[ds_name],
            akeyless_url=base_vars['akeyless_url'],
            **opts
        )

        expected_input = GetDynamicSecretValue(
            name=ds_name,
            args=opts.get('args'),
            host=opts.get('host'),
            json=False,
            target=None,
            timeout=opts.get('timeout'),
            token=opts.get('token'),
            uid_token=None
        )
        mock_api_client.get_dynamic_secret_value.assert_called_once_with(expected_input)

        assert len(response) > 0
        resp_dict = response[0]
        assert resp_dict['id'] == get_ds_value_response['id']
        assert resp_dict['password'] == get_ds_value_response['password']
        assert resp_dict['ttl_in_minutes'] == get_ds_value_response['ttl_in_minutes']
        assert resp_dict['user'] == get_ds_value_response['user']

