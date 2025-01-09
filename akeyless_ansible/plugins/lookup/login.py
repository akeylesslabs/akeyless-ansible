from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
  name: login
  version_added: 1.0.0
  description:
    - Performs a login operation against Akeyless, returning a temp token.
  extends_documentation_fragment:
    - connection
    - auth
'''

EXAMPLES = r'''
- name: Login with API Key
  set_fact:
    login_res: "{{ lookup('login',  akeyless_api_url='https://api.akeyless.io', access_type='api_key', access_id='p-12345667', access_key='the-access-key') }}"

- name: Display the temp token
  debug:
    msg:
      - "Secret Value: {{ login_res.token }}"

- name: Login with k8s
  set_fact:
    login_res: "{{ lookup('login',  akeyless_api_url='https://my.gw:8000/api/v2', access_type='k8s', access_id='p-12345667',
        k8s_service_account_token='service-account-token', k8s_auth_config_name='auth-conf-name') }}"

- name: Display the temp token
  debug:
    msg:
      - "Secret Value: {{ login_res.token }}"
'''



from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase

from ansible.errors import AnsibleError

from akeyless import ApiException


class LookupModule(AkeylessLookupBase):
    def run(self, terms, variables=None, **kwargs):
        super().run(terms, variables, **kwargs)

        if len(terms) != 0:
            self.warn("Supplied term strings will be ignored. This lookup does not use term strings.")

        self.debug("Authentication for access '%s' using auth method '%s'." % (self.get_option('access_id'), self.get_option('access_type')))

        try:
            response = self.authenticate()
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "auth"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run akeyless auth: " + str(e))

        return [response]