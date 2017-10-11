import sys, os, pwd, signal, time
from resource_management import *
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Directory, File, Link


class Master(Script):
    def install(self, env):
        # Install packages listed in metainfo.xml
        self.install_packages(env)
        self.configure(env)
        import params

        if not os.path.exists(params.install_dir):
            os.makedirs(params.install_dir)
            Execute('wget ' + params.download_url +
                    ' -O /tmp/opentsdb.tar.gz >> ' + params.log)
            Execute('tar -zxvf /tmp/opentsdb.tar.gz -C ' + params.install_dir +
                    ' >> ' + params.log)
            Execute('/bin/rm -f /tmp/opentsdb.tar.gz >> ' + params.log)
            Execute(
                'mv ' + params.install_dir + '/*/* ' + params.install_dir +
                ' >> ' + params.log,
                ignore_failures=True)
            Execute('cd ' + params.install_dir + '; ./build.sh >> ' +
                    params.log)

        if params.create_schema:
            Execute(
                'cd ' + params.install_dir +
                '; env COMPRESSION=NONE HBASE_HOME=/usr/hdp/current/hbase-client ./src/create_table.sh; >> '
                + params.log)

    def configure(self, env):
        import params
        import status_params
        env.set_params(params)
        Directory(
            [
                status_params.opentsdb_pid_dir, params.opentsdb_log_dir,
                params.install_dir
            ],
            owner=params.opentsdb_user,
            group=params.opentsdb_group)

    def stop(self, env):
        import params
        import status_params
        env.set_params(status_params)
        self.configure(env)
        Execute(
            format('pkill -TERM -P `cat {opentsdb_pidfile}` >/dev/null 2>&1'))
        Execute(format('kill `cat {opentsdb_pidfile}` >/dev/null 2>&1'))
        Execute(format("rm -f {opentsdb_pidfile}"))

    def start(self, env):
        import params
        import status_params
        self.configure(env)

        Execute('echo Starting process: ' + params.install_dir +
                params.start_cmd)
        Execute('cd ' + params.install_dir + '; nohup sh -c "' +
                params.install_dir + params.start_cmd + '" >> ' + params.log +
                ' 2>&1 & echo $! > ' + status_params.opentsdb_pid_file)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.opentsdb_pid_file)


if __name__ == "__main__":
    Master().execute()
