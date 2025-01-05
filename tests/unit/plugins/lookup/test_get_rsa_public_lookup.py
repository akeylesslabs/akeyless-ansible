from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import GetRSAPublic, GetRSAPublicOutput
from ansible.errors import AnsibleError

from ansible.plugins.loader import lookup_loader


from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def get_rsa_public_lookup():
    return lookup_loader.get('get_rsa_public')


@pytest.fixture(params=["get_rsa_public_response.json"])
def get_rsa_public_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetRSAPublicLookup(object):

    def test_is_lookup_base(self, get_rsa_public_lookup):
        assert issubclass(type(get_rsa_public_lookup), AkeylessLookupBase)

    def test_validation_error(self, get_rsa_public_lookup, base_vars):
        with pytest.raises(AnsibleError, match="secret name term is missing"):
            get_rsa_public_lookup.run(terms=[], akeyless_url=base_vars['akeyless_url'])

    def test_input_output(self, mock_api_client, get_rsa_public_lookup, get_rsa_public_response, base_vars):
        mock_api_client.get_rsa_public.return_value = GetRSAPublicOutput(**get_rsa_public_response.copy())

        key_name = "fake-rsa-key"

        opts = dict(
            token="t-123",
            uid_token="uid-321",
        )
        response = get_rsa_public_lookup.run(
            terms=[key_name],
            akeyless_url=base_vars['akeyless_url'],
            **opts
        )

        expected_input = GetRSAPublic(
            name=key_name,
            uid_token=opts.get('uid_token'),
            json=False,
            token=opts.get('token'),
        )
        mock_api_client.get_rsa_public.assert_called_once_with(expected_input)

        assert len(response) > 0
        resp_dict = response[0].to_dict()
        assert resp_dict['pem'] == get_rsa_public_response['pem']
        assert resp_dict['raw'] == get_rsa_public_response['raw']
        assert resp_dict['ssh'] == get_rsa_public_response['ssh']