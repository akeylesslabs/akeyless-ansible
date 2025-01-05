from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from unittest import mock

import pytest
from akeyless import ExportClassicKey,ExportClassicKeyOutput, ApiException
from ansible.errors import AnsibleError

from ansible.plugins.loader import lookup_loader

from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase



@pytest.fixture
def get_classic_key_lookup():
    return lookup_loader.get('get_classic_key_value')


@pytest.fixture(params=["get_ck_value_response.json"])
def get_ck_value_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetClassicKeyValueLookup(object):

    def test_get_classic_key_is_lookup_base(self, get_classic_key_lookup):
        assert issubclass(type(get_classic_key_lookup), AkeylessLookupBase)


    def test_gs_ck_value_raise_error(self, mock_api_client, get_classic_key_lookup, base_vars):
        get_classic_key_lookup.authenticate = mock.Mock(return_value=mock.Mock(token="t-123abc"))

        mock_api_client.export_classic_key.side_effect = ApiException(reason="Failed to do it", status=500)

        with pytest.raises(AnsibleError, match="API Exception when calling V2Api->export_classic_key: 500 - Failed to do it"):
            get_classic_key_lookup.run(terms=["a great ck"], akeyless_url=base_vars['akeyless_url'])


    def test_get_classic_key_value_ok(self, mock_api_client, get_classic_key_lookup, get_ck_value_response, base_vars):

        mock_api_client.export_classic_key.return_value = ExportClassicKeyOutput(**get_ck_value_response.copy())

        opts = dict(
            token="t-123",
            version=5,
            export_public_key=False,
        )

        secret_name = "foo-bar-ck"

        response = get_classic_key_lookup.run(
            terms=[secret_name],
            akeyless_url=base_vars['akeyless_url'],
            **opts
        )

        expected_get_ck_value = ExportClassicKey(
            name=secret_name,
            token=opts.get('token'),
            version=opts.get('version'),
        )

        mock_api_client.export_classic_key.assert_called_once_with(expected_get_ck_value)

        assert len(response) > 0
        resp_dict = response[0].to_dict()
        assert resp_dict['key'] == get_ck_value_response['key']
