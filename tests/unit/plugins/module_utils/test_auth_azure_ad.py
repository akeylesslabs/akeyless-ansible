from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import Auth, AuthOutput

from akeyless_ansible.plugins.module_utils._auth_method_azure_ad import AkeylessAuthMethodAzureAd
from akeyless_ansible.plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


@pytest.fixture
def access_id():
    return 'p-123azb'

@pytest.fixture
def cloud_id():
    return 'fake-cloudid-123'


@pytest.fixture
def auth_azure_ad():
    options = {
        "access_type": AkeylessAuthMethodAzureAd.NAME,
        "access_id": None,
        "cloud_id": None,
    }
    return AkeylessAuthMethodAzureAd(options)


class TestAuthAzureAd(object):

    def test_is_auth_method_base(self, auth_azure_ad):
        assert isinstance(auth_azure_ad, AkeylessAuthMethodAzureAd)
        assert issubclass(AkeylessAuthMethodAzureAd, AkeylessAuthMethodBase)

    def test_validation(self, auth_azure_ad, access_id, cloud_id):
        with pytest.raises(ValueError, match="access_id is required for the AkeylessAuthMethodAzureAd auth method"):
            auth_azure_ad.validate()

        auth_azure_ad.options['access_id'] = access_id

        with pytest.raises(ValueError, match="cloud_id is required for the AkeylessAuthMethodAzureAd auth method"):
            auth_azure_ad.validate()

        auth_azure_ad.options['cloud_id'] = cloud_id

        auth_azure_ad.validate()

    def test_input_output(self, mock_api_client, auth_azure_ad, access_id, cloud_id):
        auth_azure_ad.options['access_id'] = access_id
        auth_azure_ad.options['cloud_id'] = cloud_id

        token = "p-123"
        mock_api_client.auth.return_value = AuthOutput(token=token)

        res = auth_azure_ad.authenticate(mock_api_client)

        expected_in = Auth(
            access_id=access_id,
            cloud_id=cloud_id,
            access_type=auth_azure_ad.NAME,
        )

        assert expected_in == mock_api_client.auth.call_args[0][0]

        assert res.token == token