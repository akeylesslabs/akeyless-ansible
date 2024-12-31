from __future__ import annotations

class ModuleDocFragment(object):

    DOCUMENTATION = r'''
    options:
      access_type:
        description: Authentication method type to be used.
        choices:
          - api_key
          - password
          - saml
          - oidc
          - k8s
          - ldap
          - azure_ad
          - aws_iam
          - gcp
          - jwt
          - oci
          - cert
          - universal_identity
        default: api_key
        type: str
      access_id:
        description: The access ID for authentication.
        type: str
      access_key:
        description:  Access key (relevant only for access-type=access_key)
        type: str
      admin_password:
        description: Password (relevant only for access-type=password).
        type: str
      admin_email:
        description: Email (relevant only for access-type=password).
        type: str
      account_id:
        description: Account id (relevant only for access-type=password where the email address is associated with more than one account).
        type: str
      ldap_username:
        description: LDAP username (relevant only for access-type=ldap).
        type: str
      ldap_password:
        description: LDAP password (relevant only for access-type=ldap).
        type: str
      cloud_id:
        description: The cloud identity (relevant only for access-type=azure_ad,aws_iam,gcp,oci).
        type: str
      gcp_audience:
        description: GCP audience to use in signed JWT (relevant only for access-type=gcp).
        type: str
        default: akeyless.io
      use_remote_browser:
        description: Returns a link to complete the authentication remotely (relevant only for access-type=saml/oidc).
        type: bool
        default: false
      k8s_auth_config_name:
        description: The K8S Auth config name (relevant only for access-type=k8s).
        type: str
      k8s_service_account_token:
        description: The K8S service account token.
        type: str
      jwt:
        description: The Json Web Token (relevant only for access-type=jwt/oidc).
        type: str
      cert_data:
        description: Certificate data encoded in base64. (relevant only for access-type=cert).
        type: str
      key_data:
        description: Private key data encoded in base64 (relevant only for access-type=cert).
        type: str
      oci_auth_type:
        description: The type of the OCI configuration to use (relevant only for access-type=oci).
        choices:
          - instance
          - apikey
          - resource
        type: str
      oci_group_ocid:
        description: A list of Oracle Cloud IDs groups (relevant only for access-type=oci).
        type: list
        elements: str
      uid_token:
        description: The universal_identity token (relevant only for access-type=universal_identity).
        type: str
      gateway_url:
        description: Gateway URL relevant only for access-type=k8s/jwt/saml/oidc.
        type: str
    '''