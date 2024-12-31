from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import akeyless

DOCUMENTATION = """
  module: get_rsa_public
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
  description:
    - Obtain the public key from a specific RSA private key
  options:
    name:
      description: Name of RSA key to extract the public key from.
      type: str
      required: true
"""


from ansible.module_utils._text import to_native
from plugins.module_utils._akeyless_helper import AkeylessHelper
from plugins.module_utils._akeyless_module import AkeylessModule

from akeyless import ApiException

import traceback


def run_module():
    res = {}

    module_args = AkeylessModule.generate_argspec(
        name=dict(type='str', required=True),
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

        body = akeyless.GetRSAPublic(
            name=module.params.get('name'),
            token=token,
            uid_token=module.params.get('uid_token'),
        )
        res = module.api_client.get_rsa_public(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "get_rsa_public"),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run get_rsa_public: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True, data=res.to_dict())


def main():
    run_module()

if __name__ == '__main__':
    main()