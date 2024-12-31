import akeyless

from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodApiKey(AkeylessAuthMethodBase):
    """AkeylessAuthMethodApiKey class for auth: api_key"""

    NAME = 'api_key'

    def __init__(self, options):
        super(AkeylessAuthMethodApiKey, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['access_key'])


    def authenticate(self, api):
            body = akeyless.Auth(
                access_id=self.options.get('access_id'),
                access_type=self.NAME,
                access_key=self.options.get('access_key'),
            )

            return api.auth(body)
