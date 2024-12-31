from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import ListItems, ApiException, ListItemsOutput, ListItemsInPathOutput
from ansible.errors import AnsibleError

from ansible.plugins.loader import lookup_loader

from unittest import mock

from plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def list_lookup():
    return lookup_loader.get('list_items')

@pytest.fixture(params=["list_response.json"])
def list_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestListLookup(object):

    def test_list_is_lookup_base(self, list_lookup):
        assert issubclass(type(list_lookup), AkeylessLookupBase)


    def test_list_raise_error(self, mock_create_api_client, list_lookup, base_vars):
        mock_api_client = mock.Mock()
        mock_create_api_client.return_value = mock_api_client

        mock_response = mock.Mock()
        mock_response.token = "mock_token"
        list_lookup.authenticate = mock.Mock(return_value=mock_response)

        mock_api_client.list_items.side_effect = ApiException(status=400, reason="Somthing is not working")

        with pytest.raises(AnsibleError, match="Somthing is not working"):
            list_lookup.run(terms=[], akeyless_url=base_vars['akeyless_url'])


    def test_list_ok(self, mock_create_api_client, list_lookup, base_vars, list_response):
        mock_api_client = mock.Mock()
        mock_create_api_client.return_value = mock_api_client

        mock_api_client.list_items.return_value = ListItemsInPathOutput(**list_response.copy())

        opts = dict(
            token="t-123",
            sub_types=["XXXX"],
            filter="foobar",
            path="/x/y",
            modified_after=11,
        )

        response = list_lookup.run(
            terms=[],
            akeyless_url=base_vars['akeyless_url'],
            types=["STATIC_SECRET", "SSH_CERT_ISSUER"],
            **opts
        )

        actual_call: ListItems = mock_api_client.list_items.call_args[0][0]
        actual_call_dict =actual_call.to_dict()

        for key, value in opts.items():
            assert key in actual_call_dict, f"Key '{key}' not found in actual call."
            assert actual_call_dict[key] == value, f"Value mismatch for key '{key}': expected {value}, got {actual_call[key]}"

        assert len(response)  > 0
        resp_dict = response[0].to_dict()
        assert resp_dict['items'] == list_response['items']
        assert resp_dict['next_page'] == list_response['next_page']

