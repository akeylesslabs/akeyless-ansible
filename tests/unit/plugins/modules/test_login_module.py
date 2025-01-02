from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from unittest.mock import patch

import pytest


from akeyless import AuthOutput

import plugins.modules.login as login_module
from tests.unit.plugins.modules.test_modules_utils import  set_module_args, AnsibleExitJson, AnsibleFailJson


class TestLoginModule(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            login_module.main()

    def test_ensure_args_passed(self, mock_module_helper):
        with patch('plugins.modules.login.AkeylessModule.authenticate', return_value=AuthOutput(token="mock_token")):
            set_module_args({
                'akeyless_url': "https://xxx.com",
            })

            with pytest.raises(AnsibleExitJson) as e:
                login_module.main()

            result = e.value.args[0]
            assert result['changed'] is True
            assert result['data']['token'] == "mock_token"