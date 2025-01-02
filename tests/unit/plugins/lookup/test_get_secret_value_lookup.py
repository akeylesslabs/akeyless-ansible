from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
from unittest import mock

import pytest
from akeyless import CreateSecret, UpdateSecretVal, GetSecretValue, ApiException
from ansible.errors import AnsibleError

from ansible.plugins.loader import lookup_loader


from plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def get_secret_lookup():
    return lookup_loader.get('get_static_secret_value')

@pytest.fixture(params=["get_secret_value_response.json"])
def get_secret_value_response(request, fixture_loader):
    return fixture_loader(request.param)

class TestGetSecretValueLookup(object):

    def test_is_lookup_base(self, get_secret_lookup):
        assert issubclass(type(get_secret_lookup), AkeylessLookupBase)


    def test_raise_error(self, mock_api_client, get_secret_lookup, base_vars):
        get_secret_lookup.authenticate = mock.Mock(return_value=mock.Mock(token="t-123abc"))

        mock_api_client.get_secret_value.side_effect = ApiException("Somthing is not working")

        with pytest.raises(AnsibleError, match="API Exception when calling V2Api->get_secret_value: Somthing is not working"):
            get_secret_lookup.run(terms=["a great secret"], akeyless_url=base_vars['akeyless_url'])


    def test_validation_error(self, mock_api_client, get_secret_lookup, base_vars):
        get_secret_lookup.authenticate = mock.Mock(return_value=mock.Mock(token="t-123abc"))

        with pytest.raises(AnsibleError, match=re.escape("secret name(s) are missing")):
            get_secret_lookup.run(terms=[], akeyless_url=base_vars['akeyless_url'])


    def test_input_putput(self, mock_api_client, get_secret_lookup, get_secret_value_response, base_vars):
        mock_api_client.get_secret_value.return_value = get_secret_value_response.copy()

        opts = dict(
            uid_token="u-123332123",
            version=15,
        )

        secret_names = ["secret1", "secret2"]

        res = get_secret_lookup.run(
            terms=secret_names,
            akeyless_url=base_vars['akeyless_url'],
            **opts
        )

        mock_api_client.get_secret_value.assert_called_once_with(GetSecretValue(
            names=secret_names,
            uid_token=opts.get('uid_token'),
            version=opts.get('version'),
        ))

        assert len(res) > 0
        assert res[0] == get_secret_value_response
