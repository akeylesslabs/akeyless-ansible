from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible.errors import AnsibleError

from ansible.plugins.loader import lookup_loader

from unittest import mock

from plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase


@pytest.fixture
def login_lookup():
    return lookup_loader.get('login')

class TestLoginLookup(object):

    def test_login_is_lookup_base(self, login_lookup):
        assert issubclass(type(login_lookup), AkeylessLookupBase)

    def test_login_ok(self, login_lookup, base_vars):
        mock_response = mock.Mock()
        mock_response.token = "mock_token"
        login_lookup.authenticate = mock.Mock(return_value=mock_response)

        result = login_lookup.run(terms=[], akeyless_url=base_vars['akeyless_url'])

        assert len(result) == 1
        assert result[0].token == "mock_token"
        login_lookup.authenticate.assert_called_once()


    def test_login_with_exception(self, login_lookup, base_vars):
        login_lookup.authenticate = mock.Mock(side_effect=Exception("unknown error"))

        with pytest.raises(AnsibleError, match="Unknown exception trying to run akeyless auth: unknown error"):
            login_lookup.run(terms=[], akeyless_url=base_vars['akeyless_url'])

