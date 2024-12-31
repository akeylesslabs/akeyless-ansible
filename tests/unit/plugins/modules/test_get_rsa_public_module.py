from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
from akeyless import ApiException, GetRSAPublicOutput, GetRSAPublic

import akeyless_ansible.plugins.modules.get_rsa_public as get_rsa_public_module
from tests.unit.conftest import fixture_loader
from tests.unit.plugins.modules.test_modules_utils import set_module_args, AnsibleExitJson, AnsibleFailJson

@pytest.fixture(params=["get_rsa_public_response.json"])
def get_rsa_public_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestGetRsaPublic(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            get_rsa_public_module.main()

    def test_raise_exception_error(self, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_api_url='http://api.akeyless.test',
            access_id='a-123asdasd',
            access_type='aws_iam',
            name="xxx",
            cloud_id='c-123asdas',
        )
        set_module_args(opts)

        mock_api_client.get_rsa_public.side_effect = ApiException(reason="Some error", status=405)

        with pytest.raises(Exception, match="API Exception when calling V2Api->get_rsa_public: 405 - Some error"):
            get_rsa_public_module.main()

    def test_input_output(self, mock_api_client, mock_module_helper, get_rsa_public_response):
        opts = dict(
            akeyless_api_url='http://api.akeyless.test',
            name='test-rsa-public',
            token="t-123",
            uid_token="uid-321",
        )
        set_module_args(opts)

        mock_api_client.get_rsa_public.return_value = GetRSAPublicOutput(**get_rsa_public_response.copy())

        with pytest.raises(AnsibleExitJson) as e:
            get_rsa_public_module.main()

        mock_api_client.get_rsa_public.assert_called_once_with(GetRSAPublic(
            token=opts.get('token'),
            name=opts.get('name'),
            json=False,
            uid_token=opts.get('uid_token'),
        ))

        result = e.value.args[0]
        assert result['changed'] is True
        assert result['data'] == get_rsa_public_response