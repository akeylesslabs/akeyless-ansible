import akeyless

from akeyless_ansible.plugins.module_utils._auth_method_base import AkeylessAuthMethodBase


class AkeylessAuthMethodAwsIam(AkeylessAuthMethodBase):
    """AkeylessAuthMethodPassword class for auth: aws_iam"""

    NAME = 'aws_iam'

    def __init__(self, options):
        super(AkeylessAuthMethodAwsIam, self).__init__(options)

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
