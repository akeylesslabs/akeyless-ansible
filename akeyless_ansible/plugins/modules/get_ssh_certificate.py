#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = """
  module: get_ssh_certificate
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
    ttl:
      description: Updated certificate lifetime in seconds (must be less than the Certificate Issuer default TTL).
      type: int
    legacy_signing_alg_name:
      description: Set this option to output legacy ('ssh-rsa-cert-v01@openssh.com') signing algorithm name in the certificate.
      type: bool
      default: false
"""

EXAMPLES = r"""
- name: Generate SSH Certificate using SSH Cert Issuer "my cert issuer" singed with username "ubuntu"
  community.akeyless.get_ssh_certificate:
    akeyless_url: https://akl-url:8081
    cert_issuer_name: "my cert issuer"
    cert_username: "ubuntu"
    public_key_data: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABA"
  register: result

- name: Display the result of the operation
  ansible.builtin.debug:
    msg: "{{ result }}"
    
- name: Display the RSA key
  ansible.builtin.debug:
    msg: "{{ result.data.data }}"
"""


from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.module_utils._akeyless_module import AkeylessModule
from ansible.module_utils.common.text.converters import to_native
from akeyless import ApiException
import traceback


def run_module():
    response = {}

    module_args = AkeylessModule.generate_argspec(
        cert_username=dict(type='str', required=True),
        cert_issuer_name=dict(type='str', default=None),
        public_key_data=dict(type='str',  default=None),
        ttl=dict(type='int',  default=None),
        legacy_signing_alg_name=dict(type='bool', default=False),
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

        body = AkeylessHelper.build_get_cert_iss_body(module.params)
        response = module.api_client.get_ssh_certificate(body)
    except ApiException as e:
        module.fail_json(
            msg=AkeylessHelper.build_api_err_msg(e, "get_ssh_certificate"),
            exception=traceback.format_exc()
        )
    except Exception as e:
        module.fail_json(
            msg="Unknown exception trying to run get_ssh_certificate: " + to_native(e),
            exception=traceback.format_exc()
        )

    module.exit_json(changed=True, data=response.to_dict())


def main():
    run_module()

if __name__ == '__main__':
    main()