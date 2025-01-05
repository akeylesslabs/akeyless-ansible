from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
  name: get_dynamic_secret_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
  description:
    - Get dynamic secret value.
  options:
    _terms:
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
'''

EXAMPLES = r'''
- name: Get MySQL dynamic secret value
  set_fact:
    response: "{{ lookup('get_dynamic_secret_value', 'MyMySqlDynamicSecret', akeyless_url='https://my.gw:8000/api/v2', token='t-1233asdsad',
        target='MyMySqlTarget', args=['common_name=bar']) }}"

- name: Display the results
  debug:
    msg:
      - "Username: {{ response.user }}"
      - "Password: {{ response.password }}"
'''


from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase
from akeyless import ApiException


from ansible.errors import AnsibleError


class LookupModule(AkeylessLookupBase):
    def run(self, terms, variables=None, **kwargs):
        super().run(terms, variables, **kwargs)

        if len(terms) == 0:
            raise AnsibleError("secret name term is missing")
        name = terms[0]

        token, uid_token = self.get_option('token'), self.get_option('uid_token')

        try:
            if token is None and uid_token is None:
                auth_response = self.authenticate()
                self.set_option('token', auth_response.token)

            body = AkeylessHelper.build_get_ds_value_body(name, self._options)
            res = self.api_client.get_dynamic_secret_value(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "get_dynamic_secret_value"))
        except AttributeError as e:
            raise AnsibleError("Failed to parse get_dynamic_secret_value response: " + str(e))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run get_dynamic_secret_value: " + str(e))

        return [res]