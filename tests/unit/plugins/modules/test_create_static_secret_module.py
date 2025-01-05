from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from unittest import mock

import akeyless
import pytest
from akeyless import ApiException

import akeyless_ansible.plugins.modules.create_static_secret as create_secret_module
from tests.unit.plugins.modules.test_modules_utils import  set_module_args, AnsibleExitJson, AnsibleFailJson

class TestCreateStaticSecretModule(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            create_secret_module.main()

    def test_unsupported_params(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson) as e:
            set_module_args(dict(
                akeyless_url= 'http://api.akeyless.test',
                token='t-123asdasd',
                name="ss",
                filter="foobar",
            ))
            create_secret_module.main()
        assert "filter. Supported parameters include" in str(e.value)

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

        mock_api_client.create_secret.side_effect = ApiException(reason="Failed to create secret!", status=405)

        with pytest.raises(Exception, match="API Exception when calling V2Api->create_secret: 405 - Failed to create secret!"):
            create_secret_module.main()


    @mock.patch('akeyless_ansible.plugins.module_utils._akeyless_module.AkeylessModule.authenticate')
    def test_input_output(self, mock_authenticate, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_url= 'http://api.akeyless.test',
            token='t-123asdasd',
            name="secret-name",
            description="sdadsd",
            delete_protection='true',
            type="password",
            value="very secret val",
            format="key-value",
            urls=["a", "b"],
            password="a123",
            username="jorege",
            key="some-k",
            custom_fields=["field1", "field2"],
            tags=["tag1", "tag2", "tag3"],
            multiline=True,
            change_event='true',
        )
        set_module_args(opts)

        token = "t-15"
        auth_response = mock.Mock()
        auth_response.token = token
        mock_authenticate.return_value = auth_response

        with pytest.raises(AnsibleExitJson) as e:
            create_secret_module.main()

        mock_api_client.create_secret.assert_called_once_with(akeyless.CreateSecret(
            name=opts.get('name'),
            description=opts.get('description'),
            delete_protection=opts.get('delete_protection'),
            type=opts.get('type'),
            value=opts.get('value'),
            format=opts.get('format'),
            inject_url=opts.get('urls'),
            password=opts.get('password'),
            username=opts.get('username'),
            protection_key=opts.get('key'),
            custom_field=opts.get('custom_fields'),
            tags=opts.get('tags'),
            multiline_value=opts.get('multiline'),
            change_event=opts.get('change_event'),
            token=opts.get('token'),
        ))

        result = e.value.args[0]
        assert result['changed'] is True
        assert len(result) == 1