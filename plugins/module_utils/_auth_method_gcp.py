import akeyless

from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodGcp(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: gcp"""

    NAME = 'gcp'

    def __init__(self, options):
        super(AkeylessAuthMethodGcp, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['cloud_id'])

    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            cloud_id=self.options.get('cloud_id'),
            gcp_audience=self.options.get('gcp_audience'),
        )

        return api.auth(body)
