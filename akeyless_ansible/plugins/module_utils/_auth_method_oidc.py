import akeyless

from akeyless_ansible.plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodOidc(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: oidc"""

    NAME = 'oidc'

    def __init__(self, options):
        super(AkeylessAuthMethodOidc, self).__init__(options)

    def validate(self):
        super().validate()


    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            use_remote_browser=self.options.get('use_remote_browser'),
            jwt=self.options.get('jwt'),
            gateway_url=self.options.get('gateway_url'),
        )

        return api.auth(body)