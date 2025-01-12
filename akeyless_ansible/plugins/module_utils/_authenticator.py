from akeyless_ansible.plugins.module_utils._auth_method_api_key import AkeylessAuthMethodApiKey
from akeyless_ansible.plugins.module_utils._auth_method_aws_iam import AkeylessAuthMethodAwsIam
from akeyless_ansible.plugins.module_utils._auth_method_azure_ad import AkeylessAuthMethodAzureAd

from akeyless_ansible.plugins.module_utils._auth_method_cert import AkeylessAuthMethodCert
from akeyless_ansible.plugins.module_utils._auth_method_gcp import AkeylessAuthMethodGcp
from akeyless_ansible.plugins.module_utils._auth_method_jwt import AkeylessAuthMethodJwt
from akeyless_ansible.plugins.module_utils._auth_method_k8s import AkeylessAuthMethodK8s
from akeyless_ansible.plugins.module_utils._auth_method_ldap import AkeylessAuthMethodLdap
from akeyless_ansible.plugins.module_utils._auth_method_oci import AkeylessAuthMethodOci
from akeyless_ansible.plugins.module_utils._auth_method_oidc import AkeylessAuthMethodOidc
from akeyless_ansible.plugins.module_utils._auth_method_password import AkeylessAuthMethodPassword
from akeyless_ansible.plugins.module_utils._auth_method_saml import AkeylessAuthMethodSaml
from akeyless_ansible.plugins.module_utils._auth_method_universal_identity import AkeylessAuthMethodUniversalIdentity


class AkeylessAuthenticator:
    ARGSPEC = dict(
        access_type=dict(type='str', default='api_key', choices=[
            'api_key',
            'saml',
            'oidc',
            'k8s',
            'ldap',
            'azure_ad',
            'aws_iam',
            'gcp',
            'jwt',
            'oci',
            'cert',
            'universal_identity',
        ]),
        access_id=dict(type='str', default=None),
        access_key=dict(type='str', default=None, no_log=True),
        admin_password=dict(type='str', default=None, no_log=True),
        admin_email=dict(type='str', default=None),
        ldap_username=dict(type='str', default=None),
        ldap_password=dict(type='str', default=None, no_log=True),
        cloud_id=dict(type='str', default=None),
        gcp_audience=dict(type='str', default='akeyless.io'),
        use_remote_browser=dict(type='bool', default=False),
        k8s_auth_config_name=dict(type='str', default=None),
        k8s_service_account_token=dict(type='str', default=None),
        jwt=dict(type='str', default=None),
        cert_data=dict(type='str', default=None),
        key_data=dict(type='str', default=None, no_log=True),
        oci_auth_type=dict(type='str', default=None, choices=['instance', 'apikey', 'resource']),
        oci_group_ocid=dict(type='list', elements='str', default=None),
        uid_token=dict(type='str', default=None),
        akeyless_gateway_url=dict(type='str', default=None),
        token=dict(type='str', default=None),
    )

    def __init__(self, options):
        self._options = options
        self._selector = {
            AkeylessAuthMethodApiKey.NAME: AkeylessAuthMethodApiKey(options),
            AkeylessAuthMethodPassword.NAME: AkeylessAuthMethodPassword(options),
            AkeylessAuthMethodSaml.NAME: AkeylessAuthMethodSaml(options),
            AkeylessAuthMethodOidc.NAME: AkeylessAuthMethodOidc(options),
            AkeylessAuthMethodLdap.NAME: AkeylessAuthMethodLdap(options),
            AkeylessAuthMethodK8s.NAME: AkeylessAuthMethodK8s(options),
            AkeylessAuthMethodAzureAd.NAME: AkeylessAuthMethodAzureAd(options),
            AkeylessAuthMethodAwsIam.NAME: AkeylessAuthMethodAwsIam(options),
            AkeylessAuthMethodGcp.NAME: AkeylessAuthMethodGcp(options),
            AkeylessAuthMethodUniversalIdentity.NAME: AkeylessAuthMethodUniversalIdentity(options),
            AkeylessAuthMethodJwt.NAME: AkeylessAuthMethodJwt(options),
            AkeylessAuthMethodCert.NAME: AkeylessAuthMethodCert(options),
            AkeylessAuthMethodOci.NAME: AkeylessAuthMethodOci(options),
        }

    def validate(self):
        method = self._get_method_object()
        method.validate()

    def authenticate(self, *args, **kwargs):
        method = self._get_method_object()
        return method.authenticate(*args, **kwargs)

    def _get_method_object(self, access_type=None):
        if access_type is None:
            access_type = self._options.get('access_type')
        if access_type is None:
            raise ValueError("access_type is required and cannot be empty")
        try:
            o_auth_method = self._selector[access_type]
        except KeyError:
            raise NotImplementedError("auth method '%s' is not implemented in AkeylessAuthenticator" % access_type)

        return o_auth_method