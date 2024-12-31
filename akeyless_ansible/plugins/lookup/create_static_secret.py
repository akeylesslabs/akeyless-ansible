from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  name: create_static_secret
  version_added: 1.0.0
  extends_documentation_fragment:
    - connection
    - auth
    - token
    - accessibility
  description:
    - Creates a new static secret item.
  options:
    _terms:
      description: Secret name.
      type: str
      required: true
    description:
      description: Description of the object.
      type: str
    delete_protection:
        description: Protection from accidental deletion of this object, [true/false].
        type: str
    type:
      description: Secret type.
      type: str
      choices:
        - generic
        - password
      default: generic
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
    tags:
      description: Add tags attached to this object.
      type: list
      elements: str
    multiline:
      description: The provided value is a multiline value (separated by '\\n').
      type: bool
      default: False
    change_event:
      description: Trigger an event when a secret value changed [true/false] (Relevant only for Static Secret)
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

            body = AkeylessHelper.build_create_secret_body(name, self._options)
            self.api_client.create_secret(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "create_secret"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run create_secret: " + str(e))
