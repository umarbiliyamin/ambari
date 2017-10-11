import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core.source import InlineTemplate, Template


class Master(Script):
    def install(self, env):
        # Install packages listed in metainfo.xml
        self.install_packages(env)
        self.configure(env)
        import params

        Execute('echo "' + params.ldap_password + '" > passwd.txt')
        Execute('echo k5 >> passwd.txt')
        Execute('echo k5 >> passwd.txt')
        Execute('echo >> passwd.txt')
        try:
            Execute('kdb5_ldap_util -D ' + params.ldap_kadmind_dn +
                    ' -H ldapi:// create -r ' + params.kdc_realm +
                    ' -s< passwd.txt')
        except Exception as e:
            print(str(e))
        Execute('rm passwd.txt')

        Execute('echo "' + params.ldap_password + '" > passwd.txt')
        Execute('echo "' + params.ldap_password + '" >> passwd.txt')
        Execute('echo "' + params.ldap_password + '" >> passwd.txt')
        Execute('echo >> passwd.txt')
        Execute('kdb5_ldap_util -D ' + params.binddn +
                ' stashsrvpw -f /var/kerberos/krb5kdc/service.keyfile ' +
                params.ldap_kdc_dn + '< passwd.txt')
        Execute('kdb5_ldap_util -D ' + params.binddn +
                ' stashsrvpw -f /var/kerberos/krb5kdc/service.keyfile ' +
                params.ldap_kadmind_dn + '< passwd.txt')

        Execute('rm passwd.txt')

        Execute('/etc/rc.d/init.d/krb5kdc start')
        Execute('/etc/rc.d/init.d/kadmin start')

        Execute('chkconfig krb5kdc on')
        Execute('chkconfig kadmin on')

        Execute('echo "' + params.kdc_adminpassword + '" > passwd.txt')
        Execute('echo "' + params.kdc_adminpassword + '" >> passwd.txt')
        Execute('echo >> passwd.txt')
        Execute('kadmin.local -q "addprinc ' + params.kdc_admin +
                '" < passwd.txt')
        Execute('rm passwd.txt')

        Execute('echo "*/admin@' + params.kdc_realm +
                ' *" > /var/kerberos/krb5kdc/kadm5.acl')

    def configure(self, env):
        import params
        import status_params
        env.set_params(params)

        content = InlineTemplate(status_params.krb5_template_config)
        File(
            format("/etc/krb5.conf"),
            content=content,
            owner='root',
            group='root',
            mode=0644)

        kdc_content = Template('kdc.conf.j2')

        File(
            format("/var/kerberos/krb5kdc/kdc.conf"),
            content=kdc_content,
            owner='root',
            group='root',
            mode=0644)

    def stop(self, env):
        import params
        import status_params
        self.configure(env)

        Execute('service krb5kdc stop')
        Execute('service kadmin stop')

    def start(self, env):
        import params
        import status_params
        self.configure(env)

        Execute('service krb5kdc start')
        Execute('service kadmin start')

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status('/var/run/krb5kdc.pid')


if __name__ == "__main__":
    Master().execute()
