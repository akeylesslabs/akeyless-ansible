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

### Using the repository directly

1. Clone the repository:
   ```sh
   git clone git@github.com:akeylesslabs/akeyless-ansible.git
   cd akeyless-ansible
2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt

### Using the python package programmatically
```sh
pip install akeyless-ansible
```
   

## Usage in playbook

Example `login` with k8s using a lookup plugin:
```yaml
- name: Login K8S
  set_fact:
    login_res: "{{ lookup('login', akeyless_url=akeyless_url,
      access_type='k8s', access_id=access_id, k8s_service_account_token=k8s_service_account_token, k8s_auth_config_name=k8s_auth_config_name) }}"

- name: Display the token
  debug:
    msg:
      - "Temp token: {{ login_res.token }}"
```

Example `login` with saml:
```yaml
- name: Login saml
  login:
    akeyless_url: '{{ akeyless_url }}'
    access_type: 'saml'
    access_id: '{{ access_id }}'
  register: login_res

- name: Output authentication link
  debug:
    msg: "Please complete authentication by visiting: {{ login_res.data.complete_auth_link }}"

- name: Wait for user to complete SAML auth and input token
  pause:
    prompt: "Enter the token after completing the SAML authentication: "
  register: saml_res

- name: Display the token
  debug:
  msg:
     - "Temp token: {{ saml_token.user_input }}"
```

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
        cloud_id: '{{ cloud_id }}'
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
python -m pytest
```


## LICENSE
Licensed under MIT, see [LICENSE](LICENSE.md)