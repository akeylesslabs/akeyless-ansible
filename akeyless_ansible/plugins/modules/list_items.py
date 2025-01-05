#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = """
  module: list_items
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
    - accessibility
  description:
    - List of all accessible items.
  options:
    types:
      description: The item types list of the requested items. In case it is empty, all types of items will be returned.
      type: list[str]
    sub_types:
      description: Item sub-types (optional).
      type: list[str]
    filter:
      description: Filter by item name or part of it.
      type: str
    advanced_filter:
      description: Filter by item name/username/website or part of it.
      type: str
    path:
      description: Path to folder.
      type: str
    minimal_view:
      description: Show only basic information of the items.
      type: bool
      default: false
    pagination_token:
      description: Next page reference.
      type: str
    auto_pagination:
      description: Retrieve all items using pagination, when disabled retrieving only first 1000 items.
      type: str
      default: enabled
    modified_after:
      description: List only secrets modified after specified date (in unix time).
      type: int
    tag:
      description: Filter by item tag.
      type: str
"""


import traceback

from ansible.module_utils._text import to_native
from akeyless_ansible.plugins.module_utils._akeyless_module import AkeylessModule
from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper

from akeyless import ApiException


def run_module():
    response = {}

    module_args = AkeylessModule.generate_argspec(
        types=dict(type='list', elements='str', required=False),
        sub_types=dict(type='list', elements='str', default=None),
        filter=dict(type='str', default=None),
        advanced_filter=dict(type='str', default=None),
        path=dict(type='str', default=None),
        minimal_view=dict(type='bool', default=False),
        pagination_token=dict(type='str', default=None),
        auto_pagination=dict(type='str', default='enabled'),
        modified_after=dict(type='int', default=None),
        accessibility=dict(type='str', default='regular', choices=['regular', 'personal']),
        tag=dict(type='str', default=None),
    )

    module = AkeylessModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    token, uid_token = module.params.get('token'), module.params.get('uid_token')

    try:
        if token is None and uid_token is None:
            auth_response = module.authenticate()
            module.params['token'] = auth_response.token

        body = AkeylessHelper.build_list_items_body(module.params)

        response = module.api_client.list_items(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "list_items"),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run list_items: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True, data=response.to_dict())


def main():
    run_module()

if __name__ == '__main__':
    main()