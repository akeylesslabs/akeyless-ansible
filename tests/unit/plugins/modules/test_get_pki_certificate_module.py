from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import ApiException, GetPKICertificateOutput, GetPKICertificate

import akeyless_ansible.plugins.modules.get_pki_certificate as get_pki_certificate_module
from tests.unit.conftest import fixture_loader
from tests.unit.plugins.modules.test_modules_utils import set_module_args, AnsibleExitJson, AnsibleFailJson


@pytest.fixture(params=["get_pki_certificate_response.json"])
def get_pki_certificate_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetPkiCertificateModule(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            get_pki_certificate_module.main()


    def test_raise_exception_error(self, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_url='http://api.akeyless.test',
            access_id='a-123asdasd',
            access_type='aws_iam',
            cert_issuer_name="fake-pki-cert",
            cloud_id='c-123asdas',
        )
        set_module_args(opts)

        mock_api_client.get_pki_certificate.side_effect = ApiException(reason="Some error occured", status=402)

        with pytest.raises(Exception, match="API Exception when calling V2Api->get_pki_certificate: 402 - Some error occured"):
            get_pki_certificate_module.main()


    def test_input_output(self, mock_api_client, mock_module_helper, get_pki_certificate_response):
        opts = dict(
            akeyless_url='http://api.akeyless.test',
            token="t-123",
            cert_issuer_name="fake-pki-cert",
            key_data_base64="asdasdasd",
            csr_data_base64="ddas13d",
            common_name="somecommon-name",
            alt_names="dsaad,alt2",
            uri_sans="dds,da",
            ttl="3m",
            extended_key_usage="clientauth,serverauth",
            extra_extensions="{}",
        )
        set_module_args(opts)

        mock_api_client.get_pki_certificate.return_value = GetPKICertificateOutput(**get_pki_certificate_response.copy())

        with pytest.raises(AnsibleExitJson) as e:
            get_pki_certificate_module.main()

        mock_api_client.get_pki_certificate.assert_called_once_with(GetPKICertificate(
            cert_issuer_name=opts.get("cert_issuer_name"),
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
        ))

        result = e.value.args[0]
        assert result['changed'] is True
        assert result['data'] == get_pki_certificate_response
