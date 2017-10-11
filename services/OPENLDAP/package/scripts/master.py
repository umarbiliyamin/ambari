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

        service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

        #Ensure the shell scripts in the services dir are executable
        Execute('find ' + service_packagedir +
                ' -iname "*.sh" | xargs chmod +x')

        Execute('echo "Running ' + service_packagedir + '/scripts/setup.sh"')

        # run setup script which has simple shell setup
        Execute(service_packagedir + '/scripts/setup.sh ' +
                params.ldap_password + ' ' + params.ldap_adminuser + ' ' +
                params.ldap_domain + ' ' + params.ldap_ldifdir + ' ' + params.
                ldap_ou + ' "' + params.binddn + '" >> ' + params.stack_log)

    def configure(self, env):
        import params
        env.set_params(params)

        content = Template('slapd.j2')

        File(
            format("/etc/openldap/slapd.conf"),
            content=content,
            owner='root',
            group='root',
            mode=0644)

    def stop(self, env):
        Execute('service slapd stop')

    def start(self, env):
        Execute('service slapd start')

    def status(self, env):
        Execute('service slapd status')


if __name__ == "__main__":
    Master().execute()
