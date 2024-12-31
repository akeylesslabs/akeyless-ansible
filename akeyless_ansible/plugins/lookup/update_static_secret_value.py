from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  name: update_static_secret_value
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
    - accessibility
  description:
    - Update static secret value.
  options:
    _terms:
      description: Secret name.
      type: str
      required: true
    value:
      description: The secret value (relevant only for type 'generic').
      type: str
    format:
      description: Secret format (relevant only for type 'generic').
      type: str
      choices:
        - text
        - json
        - key-value
      default: text
    urls:
      description: List of URLs associated with the item (relevant only for type 'password')
      type: list
      elements: str
    password:
      description: Password value (relevant only for type 'password').
      type: str
    username:
      description: Username value (relevant only for type 'password')
      type: str
    key:
      description: The name of a key that used to encrypt the secret value (if empty, the account default protectionKey key will be used).
      type: str
    custom_fields:
      description: Additional custom fields to associate with the item.
      type: list
      elements: str
    multiline:
      description: The provided value is a multiline value (separated by '\\n').
      type: bool
      default: False
    last_version:
      description: The last version number before the update.
      type: int
    keep_prev_version:
      description: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings.
      type: str
"""


from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase

from ansible.errors import AnsibleError

from akeyless import ApiException


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

            body = AkeylessHelper.build_update_secret_val_body(name, self._options)
            self.api_client.update_secret_val(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "update_secret_val"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run update_secret_val: " + str(e))
