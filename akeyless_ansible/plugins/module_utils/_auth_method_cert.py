import akeyless

from akeyless_ansible.plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodCert(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: cert"""

    NAME = 'cert'

    def __init__(self, options):
        super(AkeylessAuthMethodCert, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['cert_data', 'key_data'])

    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            cert_data=self.options.get('cert_data'),
            key_data=self.options.get('key_data'),
        )

        return api.auth(body)
