from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from unittest import mock

import pytest
from akeyless import ApiException, ListItemsInPathOutput, ListItems

import akeyless_ansible.plugins.modules.list_items as list_items_module
from tests.unit.conftest import fixture_loader
from tests.unit.plugins.modules.test_modules_utils import  set_module_args, AnsibleExitJson, AnsibleFailJson

@pytest.fixture(params=["list_response.json"])
def list_response(request, fixture_loader):
    return fixture_loader(request.param)


class TestListItemsModule(object):

    def test_module_fail_when_required_args_missing(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson):
            set_module_args({})
            list_items_module.main()


    def test_unsupported_params(self, mock_module_helper):
        with pytest.raises(AnsibleFailJson) as e:
            set_module_args(dict(
                akeyless_api_url= 'http://api.akeyless.test',
                token='t-123asdasd',
                filterxxxx="foobar",
            ))
            list_items_module.main()
        assert "filterxxxx. Supported parameters include" in str(e.value)


    def test_raise_api_error(self, mock_api_client, mock_module_helper):
        opts = dict(
            akeyless_api_url= 'http://api.akeyless.test',
            access_id='a-123asdasd',
            access_type='aws_iam',
            cloud_id='c-123asdas',
        )
        set_module_args(opts)

        mock_api_client.list_items.side_effect = ApiException(reason="Some error", status=405)

        with pytest.raises(Exception, match="API Exception when calling V2Api->list_items: 405 - Some error"):
            list_items_module.main()


    @mock.patch('akeyless_ansible.plugins.module_utils._akeyless_module.AkeylessModule.authenticate')
    def test_input_output(self, mock_authenticate, mock_api_client, mock_module_helper, list_response):
        opts = dict(
            akeyless_api_url= 'http://api.akeyless.test',
            token='t-123asdasd',
            sub_types=["XXXX"],
            filter="foobar",
            path="/x/y",
            modified_after=12,
            types=["YYYY", "sss"],
        )
        set_module_args(opts)

        token = "t-15"
        auth_response = mock.Mock()
        auth_response.token = token
        mock_authenticate.return_value = auth_response

        mock_api_client.list_items.return_value = ListItemsInPathOutput(**list_response.copy())


        with pytest.raises(AnsibleExitJson) as e:
            list_items_module.main()

        mock_api_client.list_items.assert_called_once_with(ListItems(
            token=opts.get('token'),
            sub_types=opts.get('sub_types'),
            filter=opts.get('filter'),
            path=opts.get('path'),
            modified_after=opts.get('modified_after'),
            type=opts.get('types'),
            advanced_filter=None,
            auto_pagination="enabled",
            json=False,
            minimal_view=False,
            pagination_token=None,
            sra_only=False,
            tag=None,
            uid_token=None
        ))

        result = e.value.args[0]
        assert result['changed'] is True
        assert result['data']['items'] == list_response['items']
        assert result['data']['next_page'] == list_response['next_page']