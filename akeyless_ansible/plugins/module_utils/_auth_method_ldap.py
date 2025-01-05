import akeyless

from akeyless_ansible.plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodLdap(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: ldap"""

    NAME = 'ldap'

    def __init__(self, options):
        super(AkeylessAuthMethodLdap, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['ldap_username', 'ldap_password'])

    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            ldap_username=self.options.get('ldap_username'),
            ldap_password=self.options.get('ldap_password'),
        )

        return api.auth(body)
