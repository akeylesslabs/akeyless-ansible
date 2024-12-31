import akeyless

from akeyless_ansible.plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodUniversalIdentity(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: universal_identity"""

    NAME = 'universal_identity'

    def __init__(self, options):
        super(AkeylessAuthMethodUniversalIdentity, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['uid_token'])

    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            uid_token=self.options.get('uid_token'),
        )

        return api.auth(body)
