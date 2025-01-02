from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
  name: get_static_secret_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
    - accessibility
  description:
    - Get static secret value.
  options:
    _terms:
      description: Secret name(s).
      type: list
      elements: str
      required: true
    version:
      description: Secret version, if negative value N is provided (--version=-N) the last N versions will return (maximum 20).
      type: int
'''


EXAMPLES = r'''
- name: Get item secret value by name
  set_fact:
    response: "{{ lookup('get_static_secret_value', 'MySecret', akeyless_url='https://api.akeyless.io', access_type='api_key',
        access_id='p-12345667', access_key='the-access-key') }}"

- name: Display the results
  debug:
    msg:
      - "Secret Value: {{ response['MySecret'] }}"

- name: Get multiple secrets values with token
  set_fact:
    response: "{{ lookup('get_static_secret_value', 'MySecret1', 'MySecret2', akeyless_url='https://api.akeyless.io',
     token='t-123456abcdefg') }}"

- name: Display the results
  debug:
    msg:
      - "Secret1 Value: {{ response['MySecret1'] }}"
      - "Secret2 Value: {{ response['MySecret2'] }}"
'''


from plugins.module_utils._akeyless_helper import AkeylessHelper
from plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase

from ansible.errors import AnsibleError

from akeyless import ApiException


class LookupModule(AkeylessLookupBase):
    def run(self, terms, variables=None, **kwargs):
        super().run(terms, variables, **kwargs)

        if len(terms) == 0:
            raise AnsibleError("secret name(s) are missing")
        names = terms

        token, uid_token = self.get_option('token'), self.get_option('uid_token')

        try:
            if token is None and uid_token is None:
                auth_response = self.authenticate()
                self.set_option('token', auth_response.token)

            body = AkeylessHelper.build_get_secret_val_body(names, self._options)
            res = self.api_client.get_secret_value(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "get_secret_value"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run get_secret_value: " + str(e))

        return [res]