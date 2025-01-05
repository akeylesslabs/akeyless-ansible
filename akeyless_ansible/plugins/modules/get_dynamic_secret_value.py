#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  module: get_dynamic_secret_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
  description:
    - Get dynamic secret value.
  options:
    name:
      description: Secret name.
      type: str
      required: true
    host:
      description: Host. 
      type: str
    target:
      description: Target name.
      type: str
    timeout:
      description: Timeout in seconds.
      type: int
    args:
      description: Optional arguments as key=value pairs or JSON strings, e.g. ['arg1=value1', 'arg2=value2'].
      type: list
      elements: str
"""


from ansible.module_utils._text import to_native
from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.module_utils._akeyless_module import AkeylessModule

from akeyless import ApiException

import traceback



def run_module():
    response = {}

    module_args = AkeylessModule.generate_argspec(
        name=dict(type='str', required=True),
        host=dict(type='str', default=None),
        target=dict(type='str', default=None),
        timeout=dict(type='int', required=False),
        args=dict(type='list', elements='str', required=False),
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

        body = AkeylessHelper.build_get_ds_value_body(module.params.get("name"), module.params)
        response = module.api_client.get_dynamic_secret_value(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "get_dynamic_secret_value"),
            exception=traceback.format_exc()
        )
    except AttributeError as e:
        module.fail_json(
            msg="Failed to parse get_dynamic_secret_value response: " + to_native(e),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run get_dynamic_secret_value: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True, data=response)


def main():
    run_module()

if __name__ == '__main__':
    main()