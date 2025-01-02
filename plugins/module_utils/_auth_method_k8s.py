import akeyless

from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodK8s(AkeylessAuthMethodBase):
    """AkeylessAuthMethodApiKey class for auth: k8s"""

    NAME = 'k8s'

    def __init__(self, options):
        super(AkeylessAuthMethodK8s, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['k8s_service_account_token', 'k8s_auth_config_name'])


    def authenticate(self, api):
            body = akeyless.Auth(
                access_id=self.options.get('access_id'),
                access_type=self.NAME,
                k8s_service_account_token=self.options.get('k8s_service_account_token'),
                k8s_auth_config_name=self.options.get('k8s_auth_config_name'),
                gateway_url=self.options.get('gateway_url'),
            )

            return api.auth(body)
