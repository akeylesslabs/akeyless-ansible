from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = """
name: get_pki_certificate
version_added: 1.0.0
extends_documentation_fragment:
  - connection
  - auth
  - token
description:
  - Generates PKI certificate.
options:
  cert_issuer_name:
    description: "The name of the PKI certificate issuer."
    type: str
    required: true
  key_data_base64:
    description: "PKI key file contents encoded using base64."
    type: str
  csr_data_base64:
    description: "Certificate Signing Request contents encoded in base64."
    type: str
  common_name:
    description: "The common name to be included in the PKI certificate."
    type: str
  alt_names:
    description: "The Subject Alternative Names to be included in the PKI certificate."
    type: str
  uri_sans:
    description: "The URI Subject Alternative Names to be included in the PKI certificate."
    type: str
  ttl:
    description: "Updated certificate lifetime (must be less than the Certificate Issuer default TTL). Default in seconds. Supported formats: s,m,h,d."
    type: str
  extended_key_usage:
    description: >
      A comma-separated list of extended key usage requests for certificate issuance.
      Supported values: 'clientauth', 'serverauth'. If 'critical' is present, the
      extension will be marked as critical.
    type: str
  extra_extensions:
    description: A json string that defines the requested extra extensions for the certificate.
    type: str
"""


from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase
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

            body = AkeylessHelper.build_get_pki_cert_body(self._options)
            res = self.api_client.get_pki_certificate(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "get_pki_certificate"))
        except AttributeError as e:
            raise AnsibleError("Failed to parse get_pki_certificate response: " + str(e))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run get_pki_certificate: " + str(e))

        return [res]