from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from unittest import mock

import akeyless
import pytest
from akeyless import ApiException

import akeyless_ansible.plugins.modules.get_classic_key_value as get_classic_key_module
from tests.unit.conftest import fixture_loader
from tests.unit.plugins.modules.test_modules_utils import  set_module_args, AnsibleExitJson, AnsibleFailJson

@pytest.fixture(params=["get_ck_value_response.json"])
def get_ck_value_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetClassicKeyValueModule(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            get_classic_key_module.main()


    def test_raise_exception_error(self, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_api_url= 'http://api.akeyless.test',
            access_id='a-123asdasd',
            access_type='aws_iam',
            name="xxx",
            cloud_id='c-123asdas',
        )
        set_module_args(opts)

        mock_api_client.export_classic_key.side_effect = ApiException(reason="Some error", status=405)

        with pytest.raises(Exception, match="API Exception when calling V2Api->export_classic_key: 405 - Some error"):
            get_classic_key_module.main()


    @mock.patch('akeyless_ansible.plugins.module_utils._akeyless_module.AkeylessModule.authenticate')
    def test_input_output(self, mock_authenticate, mock_api_client, mock_module_helper, get_ck_value_response):
        opts = dict(
            akeyless_api_url= 'http://api.akeyless.test',
            access_id='p-531',
            access_type='k8s',
            k8s_service_account_token='my-great-sa',
            name="jorge",
            version=15,
            export_public_key=True,
            accessibility='personal',
        )
        set_module_args(opts)

        token = "t-15"
        auth_response = mock.Mock()
        auth_response.token = token
        mock_authenticate.return_value = auth_response

        mock_api_client.export_classic_key.return_value = akeyless.ExportClassicKeyOutput(**get_ck_value_response.copy())

        with pytest.raises(AnsibleExitJson) as e:
            get_classic_key_module.main()

        mock_api_client.export_classic_key.assert_called_once_with(akeyless.ExportClassicKey(
            token=token,
            name=opts.get('name'),
            version=opts.get('version'),
            export_public_key=opts.get('export_public_key'),
            json=False,
            uid_token=None,
            ignore_cache='false', # this is string and not bool, don't ask me why
            accessibility='personal',
        ))

        result = e.value.args[0]
        assert result['changed'] is True
        assert result['data'] == get_ck_value_response