from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.exceptions import ExecutionFailed
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import Template
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.get_user_call_output import get_user_call_output
from resource_management.libraries.script import Script

from rest_commands import RestCommands
from metron_service import install_metron

class RestMaster(Script):

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_metron()

    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        env.set_params(params)
        File(format("/etc/sysconfig/metron"),
             content=Template("metron.j2")
             )

        commands = RestCommands(params)
        commands.init_kafka_topics()
        if params.security_enabled and not commands.is_acl_configured():
            commands.init_kafka_acls()
            commands.set_acl_configured()

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        self.configure(env)
        commands = RestCommands(params)
        commands.start_rest_application()

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        commands = RestCommands(params)
        commands.stop_rest_application()

    def status(self, env):
        import status_params
        env.set_params(status_params)
        cmd = format('curl --max-time 3 {hostname}:{metron_rest_port}')
        try:
            get_user_call_output(cmd, user=status_params.metron_user)
        except ExecutionFailed:
            raise ComponentIsNotRunning()

    def restart(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        commands = RestCommands(params)
        commands.restart_rest_application(env)


if __name__ == "__main__":
    RestMaster().execute()
