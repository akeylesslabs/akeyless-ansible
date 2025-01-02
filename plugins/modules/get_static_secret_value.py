#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  module: get_static_secret_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
    - accessibility
  description:
    - Get static secret value.
  options:
    names:
      description: Secret name(s).
      type: list
      elements: str
      required: true
    version:
      description: Secret version, if negative value N is provided (--version=-N) the last N versions will return (maximum 20).
      type: int
"""

EXAMPLES = r'''
- name: Get item secret value by name
  get_static_secret_value:
    akeyless_url: '{{ akeyless_url }}'
    names: ['MySecret']
    token: '{{ auth_res.token }}'
  register: response

- name: Display the results
  debug:
    msg:
      - "Secret Value: {{ response['MySecret'] }}"
      
- name: Get multiple secrets values with token with aws_iam auth
  get_static_secret_value:
    akeyless_url: '{{ akeyless_url }}'
    access_type: 'aws_iam'
    access_id: '{{ access_id }}'
    cloud_id: '{{ cloud_id }}'
    names: ['MySecret1', 'MySecret2']
  register: response

- name: Display the results
  debug:
    msg:
      - "Secret Value1: {{ response['MySecret1'] }}"
      - "Secret Value2: {{ response['MySecret2'] }}"
'''


import traceback

from ansible.module_utils.common.text.converters import to_native

from plugins.module_utils._akeyless_module import AkeylessModule
from plugins.module_utils._akeyless_helper import AkeylessHelper


from akeyless import ApiException


def run_module():
    res = {}

    module_args = AkeylessModule.generate_argspec(
        names=dict(type='list', elements='str', required=True),
        accessibility=dict(type='str', default='regular', choices=['regular', 'personal']),
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

        body = AkeylessHelper.build_get_secret_val_body(module.params.get('names'), module.params)

        res = module.api_client.get_secret_value(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "get_secret_value"),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run get_secret_value: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True, data=res)

def main():
    run_module()

if __name__ == '__main__':
    main()