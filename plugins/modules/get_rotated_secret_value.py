#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  module: get_rotated_secret_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
  description:
    - Get rotated secret value.
  options:
    name:
      description: Secret name.
      type: str
      required: true
    host:
      description: Host. 
      type: str
    version:
      description: Secret version
      type: int
    host:
      description: Get rotated secret value of specific Host (relevant only for Linked Target).
      type: str
"""

from ansible.module_utils._text import to_native
from plugins.module_utils._akeyless_helper import AkeylessHelper
from plugins.module_utils._akeyless_module import AkeylessModule

from akeyless import ApiException

import traceback


def run_module():
    response = {}

    module_args = AkeylessModule.generate_argspec(
        name=dict(type='str', required=True),
        host=dict(type='str', default=None),
        version=dict(type='int', default=None),
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

        body = AkeylessHelper.build_get_rs_value_body(module.params.get("name"), module.params)
        response = module.api_client.get_rotated_secret_value(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "get_rotated_secret_value"),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run get_rotated_secret_value: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True, data=response)


def main():
    run_module()

if __name__ == '__main__':
    main()