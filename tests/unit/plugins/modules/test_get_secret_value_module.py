from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import ApiException, GetSecretValue

from tests.unit.plugins.modules.test_modules_utils import AnsibleFailJson, set_module_args, AnsibleExitJson
import akeyless_ansible.plugins.modules.get_static_secret_value as get_secret_val_module

@pytest.fixture(params=["get_secret_value_response.json"])
def get_secret_value_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetSecretValueModule(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            get_secret_val_module.main()


    def test_raise_api_error(self, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_url= 'http://api.akeyless.test',
            token="t-123",
            names=["a", "b", "c"],
        )
        set_module_args(opts)

        mock_api_client.get_secret_value.side_effect = ApiException(reason="Failed to get secret!", status=404)

        with pytest.raises(Exception, match="API Exception when calling V2Api->get_secret_value: 404 - Failed to get secret!"):
            get_secret_val_module.main()


    def test_input_output(self, mock_api_client, mock_module_helper, get_secret_value_response):
        opts = dict(
            akeyless_url= 'http://api.akeyless.test',
            names=["secret-name"],
            version=-2,
            token="t-123",
        )
        set_module_args(opts)

        mock_api_client.get_secret_value.return_value = get_secret_value_response.copy()

        with pytest.raises(AnsibleExitJson) as e:
            get_secret_val_module.main()

        mock_api_client.get_secret_value.assert_called_once_with(GetSecretValue(
            names=opts.get('names'),
            version=opts.get('version'),
            token=opts.get('token'),
        ))

        result = e.value.args[0]
        assert result['changed'] is True
        assert result['data'] == get_secret_value_response