#!/usr/bin/python


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  module: get_pki_certificate
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
  description:
    - Generates PKI certificate.
  options:
    cert_issuer_name:
      description: The name of the PKI certificate issuer.
      type: str
      required: true
    key_data_base64:
      description: PKI key file contents encoded using base64. 
      type: str
    csr_data_base64:
      description: Certificate Signing Request contents encoded in base6.
      type: str
    common_name:
      description: The common name to be included in the PKI certificate.
      type: str
    alt_names:
      description: The Subject Alternative Names to be included in the PKI certificate.
      type: str
    uri_sans:
      description: The URI Subject Alternative Names to be included in the PKI certificate.
      type: str
    ttl:
      description: Updated certificate lifetime (must be less than the Certificate Issuer default TTL). Default in seconds, supported formats are s,m,h,d.
      type: str
    extended_key_usage:
      description: A comma-separated list of extended key usage requests which will be used for certificate issuance. Supported values: 'clientauth', 'serverauth'. If critical is present the extension will be marked as critical
      type: str
    extra_extensions:
      description: A json string that defines the requested extra extensions for the certificate.
      type: str
"""


from ansible.module_utils._text import to_native
from plugins.module_utils._akeyless_helper import AkeylessHelper
from plugins.module_utils._akeyless_module import AkeylessModule

from akeyless import ApiException

import traceback



def run_module():
    response = {}

    module_args = AkeylessModule.generate_argspec(
        cert_issuer_name=dict(type='str', required=True),
        key_data_base64=dict(type='str', default=None),
        csr_data_base64=dict(type='str', default=None),
        common_name=dict(type='str', default=None),
        alt_names=dict(type='str', default=None),
        uri_sans=dict(type='str', default=None),
        ttl=dict(type='str', default=None),
        extended_key_usage=dict(type='str', default=None),
        extra_extensions=dict(type='str', default=None),
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

        body = AkeylessHelper.build_get_pki_cert_body(module.params)
        response = module.api_client.get_pki_certificate(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "get_pki_certificate"),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run get_pki_certificate: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True, data=response.to_dict())


def main():
    run_module()

if __name__ == '__main__':
    main()