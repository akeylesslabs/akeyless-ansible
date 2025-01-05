import akeyless

from akeyless_ansible.plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodJwt(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: jwt"""

    NAME = 'jwt'

    def __init__(self, options):
        super(AkeylessAuthMethodJwt, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['jwt'])

    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            jwt=self.options.get('jwt'),
            gateway_url=self.options.get('gateway_url'),
        )

        return api.auth(body)
