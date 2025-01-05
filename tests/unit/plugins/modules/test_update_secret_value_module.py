from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from unittest import mock

import pytest
from akeyless import ApiException, UpdateSecretVal

from tests.unit.plugins.modules.test_modules_utils import AnsibleFailJson, set_module_args, AnsibleExitJson
import akeyless_ansible.plugins.modules.update_static_secret_value as update_secret_val_module



class \
        TestUpdateSecretValueModule(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            update_secret_val_module.main()

    def test_unsupported_params(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson) as e:
            set_module_args(dict(
                akeyless_url= 'http://api.akeyless.test',
                token='t-123asdasd',
                name= "ss",
                someparam="foobar",
            ))
            update_secret_val_module.main()
        assert "someparam. Supported parameters include" in str(e.value)


    def test_raise_api_error(self, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_url= 'http://api.akeyless.test',
            access_id='a-123asdasd',
            access_type='gcp',
            cloud_id='c-123asdas',
            name="ss",
            value="very secret",
        )
        set_module_args(opts)

        mock_api_client.update_secret_val.side_effect = ApiException(reason="Failed to update secret!", status=500)

        with pytest.raises(Exception, match="API Exception when calling V2Api->update_secret_val: 500 - Failed to update secret!"):
            update_secret_val_module.main()


    @mock.patch('akeyless_ansible.plugins.module_utils._akeyless_module.AkeylessModule.authenticate')
    def test_input_output(self, mock_authenticate, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_url= 'http://api.akeyless.test',
            name="ss",
            token="t-123",
            value="a value",
            format="json",
            urls=["a", "b"],
            password="some-pass",
            username="dani",
            custom_fields=["x", "y", "z"],
            key="key1",
            uid_token="uid-123",
            multiline=True,
            last_version=5,
            keep_prev_version='true',
        )
        set_module_args(opts)

        token = "t-15"
        auth_response = mock.Mock()
        auth_response.token = token
        mock_authenticate.return_value = auth_response

        with pytest.raises(AnsibleExitJson) as e:
            update_secret_val_module.main()

        mock_api_client.update_secret_val.assert_called_once_with(UpdateSecretVal(
            name=opts.get('name'),
            value=opts.get('value'),
            format=opts.get('format'),
            inject_url=opts.get('urls'),
            password=opts.get('password'),
            username=opts.get('username'),
            custom_field=opts.get('custom_fields'),
            token=opts.get('token'),
            uid_token=opts.get('uid_token'),
            key=opts.get('key'),
            last_version=5,
            multiline=opts.get('multiline'),
            keep_prev_version='true',
        ))

        result = e.value.args[0]
        assert result['changed'] is True
        assert len(result) == 1