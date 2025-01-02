from __future__ import absolute_import, division, print_function
__metaclass__ = type

import akeyless
from akeyless import GetSSHCertificate, UpdateSecretVal, GetSecretValue

from akeyless.models.create_secret import CreateSecret
from akeyless.models.get_dynamic_secret_value import GetDynamicSecretValue
from akeyless.models.get_rotated_secret_value import GetRotatedSecretValue
from akeyless.models.get_pki_certificate import GetPKICertificate
from akeyless.models.export_classic_key import ExportClassicKey

from typing import Type


class AkeylessHelper:

    @staticmethod
    def create_api_client(api_url = "https://api.akeyless.io") -> Type[akeyless.V2Api]:
        """
        creates a Akeyless API client

        :param api_url: The akeyless gateway API URL
        """
        client_cfg = akeyless.Configuration(
            host = api_url
        )
        client = akeyless.ApiClient(client_cfg)

        return akeyless.V2Api(client)

    @staticmethod
    def obtain_token(authenticator, api_client):
        """
        authenticate using the authenticator and api_client and return the token

        :param authenticator: AkeylessAuthenticator object
        :param api_client: Akeyless API client
        """
        authenticator.validate()
        auth_response = authenticator.authenticate(api_client)
        return auth_response.token

    @staticmethod
    def build_api_err_msg(api_error, operation):
        """
        build api error message based on Akeyless ApiException object

        :param api_error: ApiException object
        :param operation: str
        """
        if operation is None or operation == "":
            operation = "unknown_operation"

        return (
            f"API Exception when calling V2Api->{operation}: "
            f"{api_error.status} - {api_error.reason}\n"
            f"Details: {api_error.body if hasattr(api_error, 'body') else str(api_error)}"
        )

    @staticmethod
    def build_list_items_body(params):
        """
        build the body for listing items

        :param params: Optional input parameters
        """
        return akeyless.ListItems(
            type=params.get("types"),
            sub_types=params.get("sub_types"),
            filter=params.get("filter"),
            advanced_filter=params.get("advanced_filter"),
            modified_after=params.get("modified_after"),
            path=params.get("path"),
            accessibility=params.get("accessibility"),
            auto_pagination=params.get("auto_pagination"),
            minimal_view=params.get("minimal_view"),
            pagination_token=params.get("pagination_token"),
            tag=params.get("tag"),
            token=params.get("token"),
            uid_token=params.get("uid_token"),
        )

    @staticmethod
    def build_create_secret_body(name, params):
        """
        build the body for creating a secret

        :param name: Secret Name
        :param params: Optional input parameters
        """
        return CreateSecret(
            name=name,
            accessibility=params.get("accessibility"),
            custom_field=params.get("custom_fields"),
            delete_protection=params.get("delete_protection"),
            description=params.get("description"),
            format=params.get("format"),
            tags=params.get("tags"),
            change_event=params.get("change_event"),
            type=params.get("type"),
            username=params.get("username"),
            value=params.get("value"),
            inject_url=params.get("urls"),
            multiline_value=params.get("multiline"),
            password=params.get("password"),
            protection_key=params.get("key"),
            token=params.get("token"),
            uid_token=params.get("uid_token"),
        )

    @staticmethod
    def build_update_secret_val_body(name, params):
        """
        build the body for updaing a secret value

        :param name: Secret Name
        :param params: Optional input parameters
        """
        return UpdateSecretVal(
            name=name,
            accessibility=params.get("accessibility"),
            custom_field=params.get("custom_fields"),
            last_version=params.get("last_version"),
            keep_prev_version=params.get("keep_prev_version"),
            format=params.get("format"),
            username=params.get("username"),
            value=params.get("value"),
            inject_url=params.get("urls"),
            password=params.get("password"),
            key=params.get("key"),
            token=params.get("token"),
            uid_token=params.get("uid_token"),
            multiline=params.get("multiline"),
        )

    @staticmethod
    def build_get_secret_val_body(names, params):
        """
        build the body for gettng a secret value

        :param names: List of Secret Names
        :param params: Optional input parameters
        """
        return GetSecretValue(
            names=names,
            accessibility=params.get("accessibility"),
            version=params.get("version"),
            token=params.get("token"),
            uid_token=params.get("uid_token"),
        )

    @staticmethod
    def build_get_ds_value_body(name, params):
        """
        Build the body for getting dynamic secret value

        :param name: Secret Name
        :param params: Optional input parameters
        """
        return GetDynamicSecretValue(
            name=name,
            host=params.get("host"),
            target=params.get("target"),
            args=params.get("args"),
            token=params.get("token"),
            uid_token=params.get("uid_token"),
            timeout=params.get("timeout"),
        )

    @staticmethod
    def build_get_cert_iss_body(params):
        """
        Build the body for getting ssh certificate issuer

        :param params: Input parameters
        """
        return GetSSHCertificate(
            cert_issuer_name=params.get("cert_issuer_name"),
            cert_username=params.get("cert_username"),
            legacy_signing_alg_name=params.get("legacy_signing_alg_name"),
            public_key_data=params.get("public_key_data"),
            ttl=params.get("ttl"),
            token=params.get("token"),
            uid_token=params.get("uid_token"),
        )

    @staticmethod
    def build_get_rs_value_body(name, params):
        """
        Build the body for getting rotated secret value

        :param name: Secret Name
        :param params: Optional input parameters
        """
        return GetRotatedSecretValue(
            names=name,
            version=params.get("version"),
            host=params.get("host"),
            token=params.get("token"),
            uid_token=params.get("uid_token"),
        )

    @staticmethod
    def build_get_pki_cert_body(params):
        """
        build the body for getting PKI certificate issuer

        :param params: Optional input parameters
        """
        return GetPKICertificate(
            alt_names=params.get("alt_names"),
            cert_issuer_name=params.get("cert_issuer_name"),
            common_name=params.get("common_name"),
            csr_data_base64=params.get("csr_data_base64"),
            extended_key_usage=params.get("extended_key_usage"),
            extra_extensions=params.get("extra_extensions"),
            key_data_base64=params.get("key_data_base64"),
            ttl=params.get("ttl"),
            uri_sans=params.get("uri_sans"),
            token=params.get("token"),
            uid_token=params.get("uid_token"),
        )

    @staticmethod
    def build_export_classic_key_body(name, params):
        """
        build the body for exporting classic body

        :param name: Classic key name
        :param params: Optional input parameters
        """
        return ExportClassicKey(
            name=name,
            version=params.get("version"),
            export_public_key=params.get("export_public_key"),
            token=params.get("token"),
            uid_token=params.get("uid_token"),
            accessibility=params.get("accessibility"),
        )