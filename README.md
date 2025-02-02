# Ansible Plugin

Akeyless Ansible is a collection of Ansible modules and lookup plugins for interacting with Akeyless.
It allows you to securely manage secrets and access them within your Ansible playbooks.

## Installation

### Using the repository directly

This approach involves cloning the source code repository and running the code directly.

1. Clone the repository:
   ```sh
   git clone git@github.com:akeylesslabs/akeyless-ansible.git
   cd akeyless-ansible
2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt

### Using the python package programmatically

This approach installs the plugin as a Python package from the Python Package Index (PyPI).

```sh
pip install akeyless-ansible
```

## Configuration
### Add the Python module to PYTHONPATH
By default, ansible looks for it's dependencies in `/usr/lib/pythonX.X/site-packages/ansible`, however since we are using
a custom source code our files are not located there, and we need to add the repository path to the `PYTHONPATH` environment variable before running the playbook: 
`export PYTHONPATH=${AKEYLESS_ANSIBLE_REPO_PATH}:$PYTHONPATH`

### Configure modules paths
In order to run a playbook with akeyless modules or lookup plugins, you'll need to tell ansible where it can find the source files.
In this repository there is a file called `ansible.cfg` which contains the paths relative to this repository location, if you run the playbook
from this repository location you don't need to do anything, ansible will load the `ansible.cfg` file automatically and uses the correct paths,
however if you want to run the playbook from other location you'll need to configure the correct paths. You can do it either by using 
environment variables or by using config files.
For more information about how to configure ansible, please refer to the [official ansible documentation](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#cfg).
For example, using environment variables:
```sh
export ANSIBLE_LIBRARY=${AKEYLESS_ANSIBLE_REPO_PATH}/akeyless_ansible/plugins/modules
export ANSIBLE_LOOKUP_PLUGINS=${AKEYLESS_ANSIBLE_REPO_PATH}/akeyless_ansible/plugins/lookup
export ANSIBLE_MODULE_UTILS=${AKEYLESS_ANSIBLE_REPO_PATH}/akeyless_ansible/plugins/module_utils
export ANSIBLE_DOC_FRAGMENT_PLUGINS=${AKEYLESS_ANSIBLE_REPO_PATH}/akeyless_ansible/plugins/doc_fragments

# Run the playbook
ansible-playbook playbook.yaml
```


This plugin supports the following Authentication Methods:

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

## Examples

Create a Static Secret using Ansible Playbook:
```yaml
-- name: Create Static Secret
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: create static secret item
      create_static_secret:
        akeyless_api_url: 'https://api.akeyless.io'
        name: '/Ansible/MyStaticSecret'
        value: "AnsibleSecret"
        token: '{{ auth_res.data.token }}'
      register: response
```
Where:

- `name`: the name of the Static Secret.

- `value`: the value of the Static Secret.

- `type`: The Secret type [`generic` or `password`].

- `format`: The Secret format [`text` | `json` | `key-value`].

Fetch a Static Secret using Ansible Playbook:
```yaml
-- name: Get secret value
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get item secret value by name
      get_static_secret_value:
        akeyless_api_url: 'https://api.akeyless.io'
        names: '/Ansible/MyStaticSecret'
        token: '{{ auth_res.data.token }}'
      register: response

    - name: Display the results
      debug:
        msg: "Secret Value: {{ response.data }}"
```
Where:

- `akeyless_api_url`:  Gateway URL API V2 endpoint i.e. `https://Your_GW_URL:8000/api/v2`.

- `names`: The name of the secret.

For a full list of the possible actions, [press this link](https://github.com/akeylesslabs/akeyless-ansible/tree/main/akeyless_ansible/plugins/modules).

## Dynamic Secret Example

The following will fetch a [Dynamic Secret](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) named `Ansible/MyDynamicSecret`:

```yaml dynamic_secret.yaml
- name: Get secret value
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get item secret value by name
      get_dynamic_secret_value:
        akeyless_api_url: 'https://api.akeyless.io'
        name: '/Ansible/MyDynamicSecret'
        token: '{{ auth_res.data.token }}'
      register: response

    - name: Display the results
      debug:
        msg: "Secret Value: {{ response.data }}"
```

Additional parameters for this module can be found in the [official Ansible Repository](https://github.com/akeylesslabs/akeyless-ansible/blob/main/akeyless_ansible/plugins/modules/get_dynamic_secret_value.py)

## Rotated Secret Example

The following will fetch a [Rotated Secret](https://docs.akeyless.io/docs/rotated-secrets) named `Ansible/MyRotatedSecret`:

```yaml rotated_secret.yaml
- name: Get secret value
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get item secret value by name
      get_rotated_secret_value:
        akeyless_api_url: 'https://api.akeyless.io'
        name: '/Ansible/MyRotatedSecret'
        token: '{{ auth_res.data.token }}'
      register: response

    - name: Display the results
      debug:
        msg: "Secret Value: {{ response.data }}"
```
## SSH Certificate Example

The following will issue and fetch an SSH Certificate:

```yaml SSH Certificate
- name: Get certificate value
  hosts: localhost
  tasks:
    - name: Get temp token using api-key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get SSH certificate
      get_ssh_certificate:
        akeyless_api_url: 'https://api.akeyless.io'
        cert_issuer_name: "/Ansible/cert_issuer_name"
        cert_username: "<Username>"
        public_key_data: "<public_key_data>"
        token: '{{ auth_res.data.token }}'
      register: result

    - name: Display the RSA key
      debug:
        msg: "{{ result.data.data }}"
```

Where:

- `akeyless_api_url`: Gateway URL API V2 endpoint i.e. `https://Your_GW_URL:8000/api/v2`.

- `cert_issuer_name`: The name of the **SSH Certificate Issuer**.

- `cert_username`: The username to sign in the SSH certificate.

- `public_key_data`: SSH Public Key.

- `ttl`: **Optional**, Updated certificate lifetime in seconds (must be less than the Certificate Issuer default TTL).

- `legacy_signing_alg_name`: **Optional**, Set this option to output legacy `ssh-rsa-cert-v01@openssh.com` signing algorithm name in the certificate.

## PKI Certificate Example

The following will issue and fetch a PKI certificate:

```yaml PKI Certificate.yaml
- name: Get certificate value
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get PKI certificate
      get_pki_certificate:
        akeyless_api_url: 'https://api.akeyless.io'
        cert_issuer_name: "/Ansible/pki_issuer_name"
        csr_data_base64: "<csr_data_base64>"
        token: '{{ auth_res.data.token }}'
      register: result

    - name: Display the result of the operation
      debug:
        msg: "{{ result }}"
        
    - name: Display the RSA key
      debug:
        msg: "{{ result.data.data }}"            
```

Where:

- `akeyless_api_url`: Gateway URL API V2 endpoint i.e. `https://Your_GW_URL:8000/api/v2`.

- `cert_issuer_name`: The name of the **PKI Certificate Issuer**.

- `csr_data_base64`: Certificate Signing Request contents encoded in `base64` to generate the certificate with.

Additional parameters for this module can be found in the [official Ansible Repository](https://github.com/akeylesslabs/akeyless-ansible/blob/main/akeyless_ansible/plugins/modules/get_pki_certificate.py).

### Running unit tests
```sh
python -m pytest
```


## LICENSE
Licensed under MIT, see [LICENSE](LICENSE.md)