from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import Auth, AuthOutput

from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase
from plugins.module_utils._auth_method_k8s import AkeylessAuthMethodK8s


@pytest.fixture
def access_id():
    return 'p-123azb'

@pytest.fixture
def k8s_service_account_token():
    return 'fake-sa-token'

@pytest.fixture
def k8s_auth_config_name():
    return 'my-nice-conf'

@pytest.fixture
def gateway_url():
    return 'http://my.gw:8000'


@pytest.fixture
def auth_k8s():
    options = {
        'access_type': AkeylessAuthMethodK8s.NAME,
        'access_id': None,
        'k8s_service_account_token': None,
        'k8s_auth_config_name': None,
        'gateway_url': None,
    }
    return AkeylessAuthMethodK8s(options)


class TestAuthK8s(object):

    def test_is_auth_method_base(self, auth_k8s):
        assert isinstance(auth_k8s, AkeylessAuthMethodK8s)
        assert issubclass(AkeylessAuthMethodK8s, AkeylessAuthMethodBase)

    def test_validation(self, auth_k8s, access_id, k8s_service_account_token, k8s_auth_config_name):
        with pytest.raises(ValueError, match="access_id is required for the AkeylessAuthMethodK8s auth method"):
            auth_k8s.validate()

        auth_k8s.options['access_id'] = access_id

        with pytest.raises(ValueError, match="k8s_service_account_token is required for the AkeylessAuthMethodK8s auth method"):
            auth_k8s.validate()

        auth_k8s.options['k8s_service_account_token'] = k8s_service_account_token

        with pytest.raises(ValueError, match="k8s_auth_config_name is required for the AkeylessAuthMethodK8s auth method"):
            auth_k8s.validate()

        auth_k8s.options['k8s_auth_config_name'] = k8s_auth_config_name


        auth_k8s.validate()

    def test_input_output(self, mock_api_client, auth_k8s, access_id, k8s_service_account_token, k8s_auth_config_name, gateway_url):
        auth_k8s.options['access_id'] = access_id
        auth_k8s.options['k8s_service_account_token'] = k8s_service_account_token
        auth_k8s.options['k8s_auth_config_name'] = k8s_auth_config_name
        auth_k8s.options['gateway_url'] = gateway_url

        token = "t-asdmlo222"
        mock_api_client.auth.return_value = AuthOutput(token=token)

        res = auth_k8s.authenticate(mock_api_client)

        expected_in = Auth(
            access_id=access_id,
            k8s_service_account_token=k8s_service_account_token,
            k8s_auth_config_name=k8s_auth_config_name,
            gateway_url=gateway_url,
            access_type=AkeylessAuthMethodK8s.NAME,
        )

        assert expected_in == mock_api_client.auth.call_args[0][0]

        assert res.token == token