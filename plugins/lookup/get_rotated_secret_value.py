from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = """
  name: get_rotated_secret_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
  description:
    - Get rotated secret value.
  options:
    _terms:
      description: Secret name.
      type: str
      required: true
    host:
      description: Get rotated secret value of specific Host (relevant only for Linked Target).
      type: str
    version:
      description: Secret version.
      type: int
"""


from plugins.module_utils._akeyless_helper import AkeylessHelper
from plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase
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

            body = AkeylessHelper.build_get_rs_value_body(name, self._options)
            res = self.api_client.get_rotated_secret_value(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "get_rotated_secret_value"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run get_rotated_secret_value: " + str(e))

        return [res]