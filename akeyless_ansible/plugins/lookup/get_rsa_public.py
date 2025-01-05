from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = """
  name: get_rsa_public
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
  description:
    - Obtain the public key from a specific RSA private key
  options:
    _terms:
      description: Name of RSA key to extract the public key from.
      type: str
      required: true
"""


from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase
from akeyless import ApiException

import akeyless


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

            body = akeyless.GetRSAPublic(
                name=name,
                token=token,
                uid_token=self.get_option('uid_token'),
            )
            res = self.api_client.get_rsa_public(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "get_rsa_public"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run get_rsa_public: " + str(e))

        return [res]