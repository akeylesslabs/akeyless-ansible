from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
name: list_items
version_added: 1.0.0
extends_documentation_fragment:
  - connection
  - auth
  - token
  - accessibility
description:
  - List of all accessible items.
options:
  types:
    description:
      - The item types list of the requested items. In case it is empty, all types of items will be returned.
    type: list
    elements: str
  sub_types:
    description:
      - Item sub-types (optional).
    type: list
    elements: str
  filter:
    description:
      - Filter by item name or part of it.
    type: str
  advanced_filter:
    description:
      - Filter by item name/username/website or part of it.
    type: str
  path:
    description:
      - Path to folder.
    type: str
  minimal_view:
    description:
      - Show only basic information of the items.
    type: bool
    default: false
  pagination_token:
    description:
      - Next page reference.
    type: str
  auto_pagination:
    description:
      - Retrieve all items using pagination, when disabled retrieving only first 1000 items.
    type: str
    default: enabled
  modified_after:
    description:
      - List only secrets modified after specified date (in unix time).
    type: int
  tag:
    description:
      - Filter by item tag.
    type: str
"""


from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase

from ansible.errors import AnsibleError

from akeyless import ApiException


class LookupModule(AkeylessLookupBase):
    def run(self, terms, variables=None, **kwargs):
        super().run(terms, variables, **kwargs)

        token, uid_token = self.get_option('token'), self.get_option('uid_token')

        try:
            if token is None and uid_token is None:
                auth_response = self.authenticate()
                self.set_option('token', auth_response.token)

            body = AkeylessHelper.build_list_items_body(self._options)

            res = self.api_client.list_items(body)
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "list_items"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run list_items: " + str(e))

        return [res]