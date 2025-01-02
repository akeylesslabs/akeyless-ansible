#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  module: update_static_secret_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
    - accessibility
  description:
    - Update static secret value.
  options:
    name:
      description: Secret name.
      type: str
      required: true
    value:
      description: The secret value (relevant only for type 'generic').
      type: str
    format:
      description: Secret format (relevant only for type 'generic').
      type: str
      choices:
        - text
        - json
        - key-value
      default: text
    urls:
      description: List of URLs associated with the item (relevant only for type 'password')
      type: list
      elements: str
    password:
      description: Password value (relevant only for type 'password').
      type: str
    username:
      description: Username value (relevant only for type 'password')
      type: str
    key:
      description: The name of a key that used to encrypt the secret value (if empty, the account default protectionKey key will be used).
      type: str
    custom_fields:
      description: Additional custom fields to associate with the item.
      type: list
      elements: str
    multiline:
      description: The provided value is a multiline value (separated by '\\n').
      type: bool
      default: False
    last_version:
      description: The last version number before the update.
      type: int
    keep_prev_version:
      description: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings.
      type: str
"""


import traceback

from ansible.module_utils.common.text.converters import to_native

from plugins.module_utils._akeyless_module import AkeylessModule
from plugins.module_utils._akeyless_helper import AkeylessHelper

from akeyless import ApiException


def run_module():

    module_args = AkeylessModule.generate_argspec(
        name=dict(type='str', required=True),
        accessibility=dict(type='str', default='regular', choices=['regular', 'personal']),
        value=dict(type='str', default=None),
        format=dict(type='str', default='text', choices=['text', 'json', 'key-value']),
        urls=dict(type='list', elements='str', default=None),
        password=dict(type='str', default=None, no_log=True),
        username=dict(type='str', default=None),
        key=dict(type='str', default=None),
        custom_fields=dict(type='list', elements='str', default=None),
        multiline=dict(type='bool'),
        last_version=dict(type='int', default=None),
        keep_prev_version=dict(type='str', default=None),
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

        body = AkeylessHelper.build_update_secret_val_body(module.params.get('name'), module.params)

        module.api_client.update_secret_val(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "update_secret_val"),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run update_secret_val: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True)

def main():
    run_module()

if __name__ == '__main__':
    main()