#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = """
  name: login
  version_added: 1.0.0
  author:
    - Akeyless
  description:
    - Performs a login operation against Akeyless, returning a temp token.
  extends_documentation_fragment:
    - connection
    - auth
"""


import traceback
from plugins.module_utils._akeyless_module import AkeylessModule
from ansible.module_utils.common.text.converters import to_native


def run_module():
    response = {}

    module_args = AkeylessModule.generate_argspec()

    module = AkeylessModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    try:
        response = module.authenticate()
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())

    module.exit_json(changed=True, token=response.token)


def main():
    run_module()


if __name__ == '__main__':
    main()
