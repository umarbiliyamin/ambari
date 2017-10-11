from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.logger import Logger

from elastic import elastic


class Elasticsearch(Script):
    def install(self, env):
        import params
        env.set_params(params)
        Logger.info('Install ES Master Node')
        self.install_packages(env)

    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        env.set_params(params)

        elastic()

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        stop_cmd = "service elasticsearch stop"
        print 'Stop the Master'
        Execute(stop_cmd)

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)

        self.configure(env)
        start_cmd = "service elasticsearch start"
        print 'Start the Master'
        Execute(start_cmd)

    def status(self, env):
        import params
        env.set_params(params)
        status_cmd = "service elasticsearch status"
        print 'Status of the Master'
        Execute(status_cmd)

    def restart(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        restart_cmd = "service elasticsearch restart"
        print 'Restarting the Master'
        Execute(restart_cmd)


if __name__ == "__main__":
    Elasticsearch().execute()
