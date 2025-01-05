from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import ApiException, GetRotatedSecretValue
from ansible.errors import AnsibleError

from ansible.plugins.loader import lookup_loader

from unittest import mock


from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def get_rs_value_lookup():
    return lookup_loader.get('get_rotated_secret_value')

@pytest.fixture(params=["get_rs_value_response.json"])
def get_rs_value_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestRotatedSecretValueLookup(object):

    def test_is_lookup_base(self, get_rs_value_lookup):
        assert issubclass(type(get_rs_value_lookup), AkeylessLookupBase)

    def test_raise_error(self, mock_api_client, get_rs_value_lookup, base_vars):
        get_rs_value_lookup.authenticate = mock.Mock(return_value=mock.Mock(token="t-123abc"))

        mock_api_client.get_rotated_secret_value.side_effect = ApiException("Somthing is not working")

        with pytest.raises(AnsibleError, match="API Exception when calling V2Api->get_rotated_secret_value: Somthing is not working"):
            get_rs_value_lookup.run(terms=["a great rs"], akeyless_url=base_vars['akeyless_url'])


    def test_input_output(self, mock_api_client, get_rs_value_lookup, get_rs_value_response, base_vars):
        mock_api_client.get_rotated_secret_value.return_value = get_rs_value_response.copy()

        rs_name = "fake-mysql-rs"
        opts = dict(
            token="t-123",
            host="asdsa:22",
            version=3,
        )
        response = get_rs_value_lookup.run(
            terms=[rs_name],
            akeyless_url=base_vars['akeyless_url'],
            **opts
        )

        expected_input = GetRotatedSecretValue(
            names=rs_name,
            host=opts.get('host'),
            version=opts.get('version'),
            uid_token=None,
            json=False,
            token=opts.get('token'),
        )
        mock_api_client.get_rotated_secret_value.assert_called_once_with(expected_input)

        assert len(response) > 0
        resp_dict = response[0]
        assert resp_dict['value'] == get_rs_value_response['value']

