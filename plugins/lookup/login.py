from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
  name: login
  version_added: 1.0.0
  author:
    - Akeyless
  description:
    - Performs a login operation against Akeyless, returning a temp token.
  extends_documentation_fragment:
    - connection
    - auth
"""



from plugins.module_utils._akeyless_helper import AkeylessHelper
from plugins.plugin_utils._akeyless_lookup_base import AkeylessLookupBase

from ansible.errors import AnsibleError

from akeyless import ApiException


class LookupModule(AkeylessLookupBase):
    def run(self, terms, variables=None, **kwargs):
        super().run(terms, variables, **kwargs)

        if len(terms) != 0:
            self.warn("Supplied term strings will be ignored. This lookup does not use term strings.")

        self.debug("Authentication for access '%s' using auth method '%s'." % (self.get_option('access_id'), self.get_option('access_type')))

        try:
            response = self.authenticate()
        except ApiException as e:
            raise AnsibleError(AkeylessHelper.build_api_err_msg(e, "auth"))
        except Exception as e:
            raise AnsibleError("Unknown exception trying to run akeyless auth: " + str(e))

        return [response.token]