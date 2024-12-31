from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import Auth, AuthOutput

from plugins.module_utils._auth_method_api_key import AkeylessAuthMethodApiKey
from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


@pytest.fixture
def access_id():
    return 'p-123azb'

@pytest.fixture
def access_key():
    return 'access-key-123'


@pytest.fixture
def auth_api_key():
    options = {
        'access_type': 'api_key',
        'access_id': None,
        'access_key': None,
    }
    return AkeylessAuthMethodApiKey(options)


class TestAuthApiKey(object):

    def test_is_auth_method_base(self, auth_api_key):
        assert isinstance(auth_api_key, AkeylessAuthMethodApiKey)
        assert issubclass(AkeylessAuthMethodApiKey, AkeylessAuthMethodBase)

    def test_validation(self, auth_api_key, access_id, access_key):
        auth_api_key.options['access_id'] = access_id

        with pytest.raises(ValueError, match="access_key is required for the AkeylessAuthMethodApiKey auth method"):
            auth_api_key.validate()

        auth_api_key.options['access_key'] = access_key

        auth_api_key.validate()

    def test_input_output(self, mock_api_client, auth_api_key, access_id, access_key):
        auth_api_key.options['access_id'] = access_id
        auth_api_key.options['access_key'] = access_key

        token = "p-123"
        mock_api_client.auth.return_value = AuthOutput(token=token)

        res = auth_api_key.authenticate(mock_api_client)

        expected_in = Auth(
            access_id=access_id,
            access_key=access_key,
            access_type=auth_api_key.NAME,
        )

        assert expected_in == mock_api_client.auth.call_args[0][0]

        assert res.token == token