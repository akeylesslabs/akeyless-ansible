# Akeyless Ansible

Akeyless Ansible is a collection of Ansible modules and lookup plugins for interacting with Akeyless.
It allows you to securely manage secrets and access them within your Ansible playbooks.

### Supported auth methods:
- [Api Key](https://docs.akeyless.io/docs/api-key)
- [AWS IAM](https://docs.akeyless.io/docs/aws-iam)
- [Email](https://docs.akeyless.io/docs/email)
- [GCP](https://docs.akeyless.io/docs/gcp-auth-method)
- [Kubernetes](https://docs.akeyless.io/docs/kubernetes-auth)
- [OCI IAM](https://docs.akeyless.io/docs/oci-iam)
- [LDAP](https://docs.akeyless.io/docs/ldap)
- [JWT](https://docs.akeyless.io/docs/oauth20jwt)
- [OIDC](https://docs.akeyless.io/docs/openid)
- [SAML](https://docs.akeyless.io/docs/saml)
- [Universal Identity](https://docs.akeyless.io/docs/universal-identity)

## Installation

1. Clone the repository:
   ```sh
   git clone git@github.com:akeylesslabs/akeyless-ansible.git
   cd akeyless-ansible
2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt

## Usage
Here is an example of how to use the `get_static_secret_value` module in your playbook:
```yaml
- name: Get secret value
  hosts: localhost
  tasks:
    - name: Get temp token using aws_iam auth method
      login:
        akeyless_url: '{{ akeyless_url }}'
        access_type: 'aws_iam'
        access_id: '{{ access_id }}'
        cloud_id: '{{ cloud }}'
      register: auth_res
    - name: Get item secret value by name
      get_static_secret_value:
        akeyless_url: '{{ akeyless_url }}'
        names: ['MySecret']
        token: '{{ auth_res.token }}'
      register: response

    - name: Display the results
      debug:
        msg: "Secret Value: {{ response['MySecret'] }}"
```

### Running unit tests
```sh
pytest tests
```


## LICENSE
Licensed under MIT, see [LICENSE](LICENSE.md)