from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import ApiException, GetSSHCertificateOutput, GetSSHCertificate

import plugins.modules.get_ssh_certificate as get_ssh_certificate_module
from tests.unit.conftest import fixture_loader
from tests.unit.plugins.modules.test_modules_utils import set_module_args, AnsibleExitJson, AnsibleFailJson

@pytest.fixture(params=["get_ssh_certificate_response.json"])
def get_ssh_certificate_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetSshCertificateModule(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            get_ssh_certificate_module.main()

    def test_raise_exception_error(self, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_url='http://api.akeyless.test',
            cert_issuer_name="fake-pki-cert",
            cert_username="xxx",
            public_key_data="sdaa",
            token="t-123",
        )
        set_module_args(opts)

        mock_api_client.get_ssh_certificate.side_effect = ApiException(reason="Some error", status=405)

        with pytest.raises(Exception, match="API Exception when calling V2Api->get_ssh_certificate: 405 - Some error"):
            get_ssh_certificate_module.main()

    def test_input_output(self, mock_api_client, mock_module_helper, get_ssh_certificate_response):
        opts = dict(
            token="t-123",
            akeyless_url='http://api.akeyless.test',
            cert_issuer_name="fake-pki-cert",
            cert_username="xxx",
            public_key_data="sdaa",
            ttl=23,
            legacy_signing_alg_name=True,
        )
        set_module_args(opts)

        mock_api_client.get_ssh_certificate.return_value = GetSSHCertificateOutput(**get_ssh_certificate_response.copy())

        with pytest.raises(AnsibleExitJson) as e:
            get_ssh_certificate_module.main()

        mock_api_client.get_ssh_certificate.assert_called_once_with(GetSSHCertificate(
            token=opts.get('token'),
            cert_issuer_name=opts.get('cert_issuer_name'),
            cert_username=opts.get("cert_username"),
            public_key_data=opts.get("public_key_data"),
            ttl=opts.get("ttl"),
            legacy_signing_alg_name=opts.get("legacy_signing_alg_name"),
            json=False,
            uid_token=None,
        ))

        result = e.value.args[0]
        assert result['changed'] is True
        assert result['data'] == get_ssh_certificate_response