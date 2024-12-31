#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  module: get_classic_key_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
    - accessibility
  description:
    - Returns the Classic Key material.
  options:
    name:
      description: Classic key name.
      type: str
      required: true
    version:
      description: Classic key version.
      type: int
    export_public_key:
      description: Export only the public key.
      type: bool
      default: false
"""


from plugins.module_utils._akeyless_helper import AkeylessHelper
from plugins.module_utils._akeyless_module import AkeylessModule
from ansible.module_utils.common.text.converters import to_native


from akeyless import ApiException
import traceback

def run_module():
    res = {}

    module_args = AkeylessModule.generate_argspec(
        name=dict(type='str', required=True),
        version=dict(type='int'),
        export_public_key=dict(type='bool', default=False),
        accessibility=dict(type='str', default='regular', choices=['regular', 'personal']),
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

        body = AkeylessHelper.build_export_classic_key_body(module.params.get("name"), module.params)

        res = module.api_client.export_classic_key(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "export_classic_key"),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run export_classic_key: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True, data=res.to_dict())


def main():
    run_module()

if __name__ == '__main__':
    main()