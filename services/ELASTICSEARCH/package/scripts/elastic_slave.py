from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.logger import Logger

from slave import slave


class Elasticsearch(Script):
    def install(self, env):
        import params
        env.set_params(params)
        Logger.info('Install ES Data Node')
        self.install_packages(env)

    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        env.set_params(params)
        slave()

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        stop_cmd = "service elasticsearch stop"
        print 'Stop the Slave'
        Execute(stop_cmd)

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        self.configure(env)
        start_cmd = "service elasticsearch start"
        print 'Start the Slave'
        Execute(start_cmd)

    def status(self, env):
        import params
        env.set_params(params)
        status_cmd = "service elasticsearch status"
        print 'Status of the Slave'
        Execute(status_cmd)

    def restart(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        restart_cmd = "service elasticsearch restart"
        print 'Restarting the Slave'
        Execute(restart_cmd)


if __name__ == "__main__":
    Elasticsearch().execute()
