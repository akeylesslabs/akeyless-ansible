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

EXAMPLES = r'''
- name: Login with API Key
  login:
    akeyless_url: https://my.gw:8000/api/v2
    access_type: api_key
    access_id: {{ access_id }} 
    access_key: {{ access_key }} 
  register: login_res
  
- name: Display the temp token
  debug:
    msg:
      - "Secret Value: {{ login_res.token }}"

- name: Login with K8S
  login:
    akeyless_url: https://my.gw:8000/api/v2
    access_type: k8s
    k8s_service_account_token: {{ k8s_service_account_token }} 
    k8s_auth_config_name: {{ k8s_auth_config_name }} 
  register: login_res
'''


import traceback
from akeyless_ansible.plugins.module_utils._akeyless_module import AkeylessModule
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

    module.exit_json(changed=True, data=response.to_dict())


def main():
    run_module()


if __name__ == '__main__':
    main()
