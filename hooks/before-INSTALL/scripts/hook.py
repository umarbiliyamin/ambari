"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
from shared_initialization import *
from repo_initialization import *

from resource_management.core.resources.packaging import Package
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import default
from resource_management.core.exceptions import Fail

def ldap_client_conf():
    ldap_url = ''
    basedn = default('openldap-config/ldap.domain', 'dc=meizu,dc=com')
    ldap_hosts = default('clusterHostInfo/openldap_master_hosts', [])
    ldap_hosts_input = default('configurations/airflow-env/ldap_hosts', '')
    if len(ldap_hosts) > 0:
        ldap_url = ['ldap://' + item + '/' for item in ldap_hosts]
        ldap_url = ' '.join(ldap_url)
    elif ldap_hosts_input.strip() != '':
        ldap_hosts = ldap_hosts_input.split(' ')
        ldap_url = ['ldap://' + item + '/' for item in ldap_hosts]
        ldap_url = ' '.join(ldap_url)
    if len(ldap_url) > 0:
        Execute("mkdir -p /etc/openldap/cacerts")
        Execute(
            '/usr/sbin/authconfig --enablekrb5 --enableshadow --useshadow --enablelocauthorize --enableldap --enableldapauth --ldapserver="' + ldap_url + '" --ldapbasedn="' + basedn + '" --update')
    else:
        raise Fail(u'ldap地址为空 请先填写ldap地址 或 安装ldap')

def kerberos_client_conf():
    kerberos_host = default('clusterHostInfo/krb5_master_hosts', [])
    realm = default('configurations/krb5-config/kdc.realm', 'MEIZU.COM')
    kdc_hosts = default('configurations/airflow-env/kdc_hosts', '')
    if len(kerberos_host) > 0:
        Execute('/usr/sbin/authconfig --enablekrb5 --krb5kdc="' + ' '.join(
            kerberos_host) + '"  --krb5adminserver="' + ' '.join(
            kerberos_host) + '"  --krb5realm="' + realm + '"  --update')
    elif kdc_hosts.strip() != '':
        Execute('/usr/sbin/authconfig --enablekrb5 --krb5kdc="' + kdc_hosts + '"  --krb5adminserver="' + kdc_hosts + '"  --krb5realm="' + realm + '"  --update')
    else:
        raise Fail(u'ldap地址为空 请先填写KDC地址或 安装KDC')


def install_other_packages():
    import params
    if params.host_sys_prepped:
        return
    packages = [
        'unzip', 'curl', 'jdk', 'java-1.8.0-openjdk-devel', 'openldap-clients',
        'nss-pam-ldapd', 'pam_ldap', 'pam_krb5', 'authconfig', 'krb5-libs'
    ]
    Package(
        packages,
        retry_on_repo_unavailability=params.
        agent_stack_retry_on_unavailability,
        retry_count=params.agent_stack_retry_count)


class BeforeInstallHook(Hook):
    def hook(self, env):
        import params

        self.run_custom_hook('before-ANY')
        env.set_params(params)

        install_repos()
        install_packages()

        #extension
        install_other_packages()
        ldap_client_conf()


if __name__ == "__main__":
    BeforeInstallHook().execute()
