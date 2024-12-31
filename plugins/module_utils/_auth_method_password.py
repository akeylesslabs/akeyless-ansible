import akeyless

from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodPassword(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: password"""

    NAME = 'password'

    def __init__(self, options):
        super(AkeylessAuthMethodPassword, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['admin_password', 'admin_email'])

    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            admin_password=self.options.get('admin_password'),
            admin_email=self.options.get('admin_email'),
            account_id=self.options.get('account_id'),
        )

        return api.auth(body)
