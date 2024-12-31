#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  module: create_static_secret
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
  description:
    - Creates a new static secret item.
  options:
    name:
      description: Secret name.
      type: str
      required: true
    description:
      description: Description of the object.
      type: str
    accessibility:
      description: In case of an item in a user's personal folder.
      type: str
      choices:
        - regular
        - personal
      default: regular
    delete_protection:
        description: Protection from accidental deletion of this object, [true/false].
        type: str
    type:
      description: Secret type.
      type: str
      choices:
        - generic
        - password
      default: generic
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
    tags:
      description: Add tags attached to this object.
      type: list
      elements: str
    multiline:
      description: The provided value is a multiline value (separated by '\\n').
      type: bool
      default: False
    change_event:
      description: Trigger an event when a secret value changed [true/false] (Relevant only for Static Secret)
      type: str
"""

import traceback

from ansible.module_utils._text import to_native
from akeyless_ansible.plugins.module_utils._akeyless_module import AkeylessModule
from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless import ApiException


def run_module():

    module_args = AkeylessModule.generate_argspec(
        name=dict(type='str', required=True),
        description=dict(type='str', default=None),
        accessibility=dict(type='str', default='regular', choices=['regular', 'personal']),
        delete_protection=dict(type='str', defulat=None),
        type=dict(type='str', default='generic', choices=['generic', 'password']),
        format=dict(type='str', default='text', choices=['text', 'json', 'key-value']),
        value=dict(type='str', defalt=None),
        urls=dict(type='list', elements='str', default=None),
        password=dict(type='str', default=None, no_log=True),
        username=dict(type='str', default=None),
        key=dict(type='str', default=None),
        custom_fields=dict(type='list', elements='str', default=None),
        tags=dict(type='list', elements='str', default=None),
        multiline=dict(type='bool'),
        change_event=dict(type='str', default=None),
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

        body = AkeylessHelper.build_create_secret_body(module.params.get("name"), module.params)

        module.api_client.create_secret(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "create_secret"),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run create_secret: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True)


def main():
    run_module()

if __name__ == '__main__':
    main()