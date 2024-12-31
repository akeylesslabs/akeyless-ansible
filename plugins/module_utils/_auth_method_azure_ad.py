import akeyless

from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodAzureAd(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: azure_ad"""

    NAME = 'azure_ad'

    def __init__(self, options):
        super(AkeylessAuthMethodAzureAd, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['cloud_id'])

    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            cloud_id=self.options.get('cloud_id'),
        )

        return api.auth(body)
