from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
  name: get_ssh_certificate
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
  description:
    - Generates SSH certificate.
  options:
    cert_username:
      description: The username to sign in the SSH certificate (use a comma-separated list for more than one username).
      type: str
      required: true
    cert_issuer_name:
      description: The name of the SSH certificate issuer. 
      type: str
      required: true
    public_key_data:
      description: SSH public key contents.
      type: str
      required: true
    ttl:
      description: Updated certificate lifetime in seconds (must be less than the Certificate Issuer default TTL).
      type: int
    legacy_signing_alg_name:
      description: Set this option to output legacy ('ssh-rsa-cert-v01@openssh.com') signing algorithm name in the certificate.
      type: bool
      default: false
"""


from plugins.module_utils._akeyless_helper import AkeylessHelper
from plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase
from akeyless import ApiException


from ansible.errors import AnsibleError


class LookupModule(AkeylessLookupBase):
    def run(self, terms, variables=None, **kwargs):
        super().run(terms, variables, **kwargs)

        token, uid_token = self.get_option('token'), self.get_option('uid_token')

        try:
            if token is None and uid_token is None:
                auth_response = self.authenticate()
                self.set_option('token', auth_response.token)

            body = AkeylessHelper.build_get_cert_iss_body(self._options)
            res = self.api_client.get_ssh_certificate(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "get_ssh_certificate"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run get_ssh_certificate: " + str(e))

        return [res]