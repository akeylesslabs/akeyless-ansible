from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import Auth, AuthOutput

from plugins.module_utils._auth_method_api_key import AkeylessAuthMethodApiKey
from plugins.module_utils._auth_method_aws_iam import AkeylessAuthMethodAwsIam
from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


@pytest.fixture
def access_id():
    return 'p-123azb'

@pytest.fixture
def cloud_id():
    return 'fake-cloudid-123'


@pytest.fixture
def auth_aws_iam():
    options = {
        "access_type": AkeylessAuthMethodAwsIam.NAME,
        "access_id": None,
        "cloud_id": None,
    }
    return AkeylessAuthMethodAwsIam(options)


class TestAuthAwsIam(object):

    def test_is_auth_method_base(self, auth_aws_iam):
        assert isinstance(auth_aws_iam, AkeylessAuthMethodAwsIam)
        assert issubclass(AkeylessAuthMethodAwsIam, AkeylessAuthMethodBase)

    def test_validation(self, auth_aws_iam, access_id, cloud_id):
        with pytest.raises(ValueError, match="access_id is required for the AkeylessAuthMethodAwsIam auth method"):
            auth_aws_iam.validate()

        auth_aws_iam.options['access_id'] = access_id

        with pytest.raises(ValueError, match="cloud_id is required for the AkeylessAuthMethodAwsIam auth method"):
            auth_aws_iam.validate()

        auth_aws_iam.options['cloud_id'] = cloud_id

        auth_aws_iam.validate()

    def test_input_output(self, mock_api_client, auth_aws_iam, access_id, cloud_id):
        auth_aws_iam.options['access_id'] = access_id
        auth_aws_iam.options['cloud_id'] = cloud_id

        token = "p-123"
        mock_api_client.auth.return_value = AuthOutput(token=token)

        res = auth_aws_iam.authenticate(mock_api_client)

        expected_in = Auth(
            access_id=access_id,
            cloud_id=cloud_id,
            access_type=auth_aws_iam.NAME,
        )

        assert expected_in == mock_api_client.auth.call_args[0][0]

        assert res.token == token