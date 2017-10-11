from resource_management.core.resources.system import Directory, Execute, File
from resource_management.libraries.script.script import Script
from resource_management.core.source import Template, InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status
from flower import install_airflow


class Webserver(Script):
    def install(self, env):
        print "Installing Airflow"
        install_airflow(first=True)
        Execute("yum install -y redis")

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.airflow_config_path,
            content=InlineTemplate(params.airflow_conf),
            mode=0755)
        File(params.airflow_env_path, content=Template("airflow"), mode=0755)
        Execute('source ' + params.airflow_env_path + ';' + params.install_dir + "/bin/airflow initdb")

    def start(self, env):
        install_airflow()
        self.configure(env)
        import params
        Execute(" rm -rf " + params.webserver_pid , user=params.airflow_user)
        Execute(
            'source ' + params.airflow_env_path + "; source " + params.install_dir + "/bin/activate; nohup " + params.install_dir + '/bin/airflow webserver -D --pid ' + params.webserver_pid + ' -l ' + params.airflow_base_log_folder + '/webserver.log &',
            user=params.airflow_user)

    def stop(self, env):
        import params
        Execute(" kill -9 `cat " + params.webserver_pid + "`", user=params.airflow_user)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.webserver_pid)


if __name__ == "__main__":
    Webserver().execute()
