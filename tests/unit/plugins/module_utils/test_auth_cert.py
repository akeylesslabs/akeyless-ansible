from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import Auth, AuthOutput

from akeyless_ansible.plugins.module_utils._auth_method_base import AkeylessAuthMethodBase
from akeyless_ansible.plugins.module_utils._auth_method_cert import AkeylessAuthMethodCert



@pytest.fixture
def access_id():
    return 'p-123azb'

@pytest.fixture
def cert_data():
    return 'fake-cert-data'

@pytest.fixture
def key_data():
    return 'fake-key-data'


@pytest.fixture
def auth_cert():
    options = {
        'access_type': AkeylessAuthMethodCert.NAME,
        'access_id': None,
        'cert_data': None,
        'key_data': None,
    }
    return AkeylessAuthMethodCert(options)


class TestAuthCert(object):

    def test_is_auth_method_base(self, auth_cert):
        assert isinstance(auth_cert, AkeylessAuthMethodCert)
        assert issubclass(AkeylessAuthMethodCert, AkeylessAuthMethodBase)

    def test_validation(self, auth_cert, access_id, cert_data, key_data):
        with pytest.raises(ValueError, match="access_id is required for the AkeylessAuthMethodCert auth method"):
            auth_cert.validate()

        auth_cert.options['access_id'] = access_id

        with pytest.raises(ValueError, match="cert_data is required for the AkeylessAuthMethodCert auth method"):
            auth_cert.validate()

        auth_cert.options['cert_data'] = cert_data

        with pytest.raises(ValueError, match="key_data is required for the AkeylessAuthMethodCert auth method"):
            auth_cert.validate()

        auth_cert.options['key_data'] = key_data

        auth_cert.validate()

    def test_input_output(self, mock_api_client, auth_cert, access_id, cert_data, key_data):
        auth_cert.options['access_id'] = access_id
        auth_cert.options['cert_data'] = cert_data
        auth_cert.options['key_data'] = key_data

        token = "p-123"
        mock_api_client.auth.return_value = AuthOutput(token=token)

        res = auth_cert.authenticate(mock_api_client)

        expected_in = Auth(
            access_id=access_id,
            cert_data=cert_data,
            key_data=key_data,
            access_type=AkeylessAuthMethodCert.NAME,
        )

        assert expected_in == mock_api_client.auth.call_args[0][0]

        assert res.token == token