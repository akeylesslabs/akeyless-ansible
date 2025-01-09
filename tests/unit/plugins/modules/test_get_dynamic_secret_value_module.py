from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import ApiException, GetDynamicSecretValue

import akeyless_ansible.plugins.modules.get_dynamic_secret_value as get_dynamic_secret_module
from tests.unit.conftest import fixture_loader
from tests.unit.plugins.modules.test_modules_utils import set_module_args, AnsibleExitJson, AnsibleFailJson

@pytest.fixture(params=["get_ds_value_response.json"])
def get_ds_value_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetDynamicSecretValue(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            get_dynamic_secret_module.main()


    def test_raise_exception_error(self, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_api_url='http://api.akeyless.test',
            access_id='a-123asdasd',
            access_type='aws_iam',
            name="xxx",
            cloud_id='c-123asdas',
        )
        set_module_args(opts)

        mock_api_client.get_dynamic_secret_value.side_effect = ApiException(reason="Some error", status=405)

        with pytest.raises(Exception, match="API Exception when calling V2Api->get_dynamic_secret_value: 405 - Some error"):
            get_dynamic_secret_module.main()


    def test_input_output(self, mock_api_client, mock_module_helper, get_ds_value_response):
        opts = dict(
            akeyless_api_url='http://api.akeyless.test',
            token="p-1233333",
            name='test-secret',
            host='remotehost',
            target='k8s',
            timeout=54,
            args=["key1=val3", "key4=val55"],
        )
        set_module_args(opts)


        mock_api_client.get_dynamic_secret_value.return_value = get_ds_value_response.copy()

        with pytest.raises(AnsibleExitJson) as e:
            get_dynamic_secret_module.main()

        mock_api_client.get_dynamic_secret_value.assert_called_once_with(GetDynamicSecretValue(
            token="p-1233333",
            name=opts.get('name'),
            host=opts.get('host'),
            target=opts.get('target'),
            json=False,
            uid_token=None,
            timeout=opts.get('timeout'),
            args=opts.get('args'),
        ))

        result = e.value.args[0]
        assert result['changed'] is True
        assert result['data'] == get_ds_value_response