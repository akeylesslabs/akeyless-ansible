from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from akeyless import GetSSHCertificateOutput, GetSSHCertificate
from ansible.errors import AnsibleError

from ansible.plugins.loader import lookup_loader

from unittest import mock


from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def get_rsa_public_lookup():
    return lookup_loader.get('get_ssh_certificate')


@pytest.fixture(params=["get_ssh_certificate_response.json"])
def get_ssh_certificate_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetSShCertificateLookup(object):

    def test_is_lookup_base(self, get_rsa_public_lookup):
        assert issubclass(type(get_rsa_public_lookup), AkeylessLookupBase)

    def test_validation_error(self, get_rsa_public_lookup, base_vars):
        get_rsa_public_lookup.authenticate = mock.Mock(return_value=mock.Mock(token="t-123abc"))

        with pytest.raises(AnsibleError, match="lookup plugin: get_ssh_certificate setting: cert_username"):
            get_rsa_public_lookup.run(terms=[], akeyless_url=base_vars['akeyless_url'])

    def test_input_output(self, mock_api_client, get_rsa_public_lookup, get_ssh_certificate_response, base_vars):
        mock_api_client.get_ssh_certificate.return_value = GetSSHCertificateOutput(**get_ssh_certificate_response.copy())

        opts = dict(
            token="t-123",
            cert_issuer_name="fake-pki-cert",
            cert_username="xxx",
            public_key_data="sdaa",
            ttl=23,
            legacy_signing_alg_name=True,
        )
        response = get_rsa_public_lookup.run(
            terms=[],
            akeyless_url=base_vars['akeyless_url'],
            **opts
        )

        expected_input = GetSSHCertificate(
            token=opts.get('token'),
            cert_issuer_name=opts.get('cert_issuer_name'),
            cert_username=opts.get("cert_username"),
            public_key_data=opts.get("public_key_data"),
            ttl=opts.get("ttl"),
            legacy_signing_alg_name=opts.get("legacy_signing_alg_name"),
            json=False,
            uid_token=None,
        )
        mock_api_client.get_ssh_certificate.assert_called_once_with(expected_input)

        assert len(response) > 0
        resp_dict = response[0].to_dict()
        assert resp_dict['data'] == get_ssh_certificate_response['data']
        assert resp_dict['path'] == get_ssh_certificate_response['path']