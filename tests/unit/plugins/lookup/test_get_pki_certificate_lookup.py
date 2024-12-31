from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import akeyless
import pytest
from akeyless import GetPKICertificate
from ansible.errors import AnsibleError

from ansible.plugins.loader import lookup_loader

from unittest import mock


from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def get_pki_cert_lookup():
    return lookup_loader.get('get_pki_certificate')


@pytest.fixture(params=["get_pki_certificate_response.json"])
def get_pki_cert_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetPkiCertificateLookup(object):

    def test_is_lookup_base(self, get_pki_cert_lookup):
        assert issubclass(type(get_pki_cert_lookup), AkeylessLookupBase)


    def test_validation_error(self, mock_api_client, get_pki_cert_lookup, base_vars):
        get_pki_cert_lookup.authenticate = mock.Mock(return_value=mock.Mock(token="t-123abc"))

        with pytest.raises(AnsibleError, match="No setting was provided for required configuration plugin_type: lookup plugin: get_pki_certificate setting: cert_issuer_name"):
            get_pki_cert_lookup.run(terms=[], akeyless_api_url=base_vars['akeyless_api_url'])


    def test_input_output(self, mock_api_client, get_pki_cert_lookup, get_pki_cert_response, base_vars):
        mock_api_client.get_pki_certificate.return_value = akeyless.GetPKICertificateOutput(**get_pki_cert_response.copy())

        cert_name = "fake-pki-cert"

        opts = dict(
            token="t-123",
            cert_issuer_name=cert_name,
            key_data_base64="asdasdasd",
            csr_data_base64="ddas13d",
            common_name="somecommon-name",
            alt_names="dsaad,alt2",
            uri_sans="dds,da",
            ttl="3m",
            extended_key_usage="clientauth,serverauth",
            extra_extensions="{}",
        )
        response = get_pki_cert_lookup.run(
            terms=[],
            akeyless_api_url=base_vars['akeyless_api_url'],
            **opts
        )

        expected_input = GetPKICertificate(
            cert_issuer_name=cert_name,
            key_data_base64=opts.get('key_data_base64'),
            csr_data_base64=opts.get('csr_data_base64'),
            common_name=opts.get('common_name'),
            alt_names=opts.get('alt_names'),
            uri_sans=opts.get('uri_sans'),
            ttl=opts.get('ttl'),
            extended_key_usage=opts.get('extended_key_usage'),
            uid_token=None,
            json=False,
            extra_extensions=opts.get('extra_extensions'),
            token=opts.get('token'),
        )
        mock_api_client.get_pki_certificate.assert_called_once_with(expected_input)

        assert len(response) > 0
        resp_dict = response[0].to_dict()
        assert resp_dict['data'] == get_pki_cert_response['data']
        assert resp_dict['cert_item_id'] == get_pki_cert_response['cert_item_id']

