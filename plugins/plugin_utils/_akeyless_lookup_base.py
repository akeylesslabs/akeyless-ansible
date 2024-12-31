from __future__ import absolute_import, division, print_function
__metaclass__ = type

import akeyless
from ansible.plugins.lookup import LookupBase

from plugins.module_utils._akeyless_helper import AkeylessHelper
from plugins.module_utils._authenticator import AkeylessAuthenticator
from plugins.plugin_utils._akeyless_plugin import AkeylessPlugin



class AkeylessLookupBase(AkeylessPlugin, LookupBase):
    def __init__(self, loader=None, templar=None, **kwargs):
        AkeylessPlugin.__init__(self)
        LookupBase.__init__(self, loader=loader, templar=templar, **kwargs)
        self.authenticator: AkeylessAuthenticator = None
        self.api_client: akeyless.V2Api = None

    def run(self, terms, variables=None, **kwargs):
        self.set_options(direct=kwargs, var_options=variables)

        # we're setting the dependencies here since in the __ini__ the options are not set yet
        self.authenticator = AkeylessAuthenticator(self._options)
        self.api_client = AkeylessHelper.create_api_client(self.get_option('akeyless_url'))

    def authenticate(self):
        self.authenticator.validate()
        return self.authenticator.authenticate(self.api_client)