import akeyless

from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodSaml(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: saml"""

    NAME = 'saml'

    def __init__(self, options):
        super(AkeylessAuthMethodSaml, self).__init__(options)

    def validate(self):
        super().validate()


    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            use_remote_browser=self.options.get('use_remote_browser'),
            gateway_url=self.options.get('gateway_url'),
        )

        return api.auth(body)