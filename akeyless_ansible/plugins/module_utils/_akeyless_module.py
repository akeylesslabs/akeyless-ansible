from __future__ import absolute_import, division, print_function
__metaclass__ = type

import akeyless
from ansible.module_utils.basic import *

from akeyless_ansible.plugins.module_utils._akeyless_helper import AkeylessHelper
from akeyless_ansible.plugins.module_utils._authenticator import AkeylessAuthenticator

class AkeylessModule(AnsibleModule):
    ARGSPEC = dict(
        akeyless_url=dict(type='str', required=True),
    )

    def __init__(self, *args, **kwargs):
        super(AkeylessModule, self).__init__(*args, **kwargs)
        self.authenticator: AkeylessAuthenticator = AkeylessAuthenticator(self.params)
        self.api_client: akeyless.V2Api = AkeylessHelper.create_api_client(self.params.get('akeyless_url'))


    def authenticate(self):
        self.authenticator.validate()
        return self.authenticator.authenticate(self.api_client)


    @classmethod
    def generate_argspec(cls, **kwargs):
        spec = cls.ARGSPEC.copy()
        spec.update(AkeylessAuthenticator.ARGSPEC.copy())
        spec.update(**kwargs)

        return spec





