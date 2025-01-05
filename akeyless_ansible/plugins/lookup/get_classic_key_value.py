from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: get_classic_key_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
    - accessibility
  description:
    - Returns the Classic Key material.
  options:
    _terms:
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


from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase

from ansible.errors import AnsibleError

from akeyless import ApiException

class LookupModule(AkeylessLookupBase):
    def run(self, terms, variables=None, **kwargs):
        super().run(terms, variables, **kwargs)

        if len(terms) == 0:
            raise AnsibleError("classic key name term is missing")
        name = terms[0]

        token, uid_token = self.get_option('token'), self.get_option('uid_token')

        try:
            if token is None and uid_token is None:
                auth_response = self.authenticate()
                self.set_option('token', auth_response.token)

            body = AkeylessHelper.build_export_classic_key_body(name, self._options)

            res = self.api_client.export_classic_key(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "export_classic_key"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run export_classic_key: " + str(e))

        return [res]