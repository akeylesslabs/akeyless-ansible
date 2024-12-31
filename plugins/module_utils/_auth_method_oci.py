import akeyless

from plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodOci(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: oci"""

    NAME = 'oci'

    def __init__(self, options):
        super(AkeylessAuthMethodOci, self).__init__(options)

    def validate(self):
        super().validate()
        self.validate_required_options(['oci_auth_type'])

    def authenticate(self, api):
        body = akeyless.Auth(
            access_id=self.options.get('access_id'),
            access_type=self.NAME,
            oci_auth_type=self.options.get('oci_auth_type'),
            oci_group_ocid=self.options.get('oci_group_ocid'),
        )

        return api.auth(body)

