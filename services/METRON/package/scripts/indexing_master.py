import os
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import File
from resource_management.core.source import Template
from resource_management.libraries.functions.format import format
from resource_management.core.source import StaticFile
from resource_management.libraries.functions import format as ambari_format
from resource_management.libraries.script import Script

from metron_security import storm_security_setup
import metron_service
from indexing_commands import IndexingCommands
from metron_service import install_metron

class Indexing(Script):
    __configured = False

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_metron()

    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        env.set_params(params)

        Logger.info("Running indexing configure")
        File(format("{metron_config_path}/elasticsearch.properties"),
             content=Template("elasticsearch.properties.j2"),
             owner=params.metron_user,
             group=params.metron_group
             )

        if not metron_service.is_zk_configured(params):
            metron_service.init_zk_config(params)
            metron_service.set_zk_configured(params)
        metron_service.refresh_configs(params)

        commands = IndexingCommands(params)
        if not commands.is_configured():
            commands.init_kafka_topics()
            commands.init_hdfs_dir()
            commands.set_configured()
        if params.security_enabled and not commands.is_hdfs_perm_configured():
            # If we Kerberize the cluster, we need to call this again, to remove write perms from hadoop group
            # If we start off Kerberized, it just does the same thing twice.
            commands.init_hdfs_dir()
            commands.set_hdfs_perm_configured()
        if params.security_enabled and not commands.is_acl_configured():
            commands.init_kafka_acls()
            commands.set_acl_configured()

        if not commands.is_hbase_configured():
            commands.create_hbase_tables()
        if params.security_enabled and not commands.is_hbase_acl_configured():
            commands.set_hbase_acls()

        Logger.info("Calling security setup")
        storm_security_setup(params)

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        self.configure(env)
        commands = IndexingCommands(params)
        commands.start_indexing_topology(env)

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        commands = IndexingCommands(params)
        commands.stop_indexing_topology(env)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        commands = IndexingCommands(status_params)
        if not commands.is_topology_active(env):
            raise ComponentIsNotRunning()

    def restart(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        commands = IndexingCommands(params)
        commands.restart_indexing_topology(env)

    def elasticsearch_template_install(self, env):
        import params
        env.set_params(params)

        File(params.bro_index_path,
             mode=0755,
             content=StaticFile('bro_index.template')
             )

        File(params.snort_index_path,
             mode=0755,
             content=StaticFile('snort_index.template')
             )

        File(params.yaf_index_path,
             mode=0755,
             content=StaticFile('yaf_index.template')
             )

        File(params.error_index_path,
             mode=0755,
             content=StaticFile('error_index.template')
             )

        File(params.meta_index_path,
             mode=0755,
             content=StaticFile('meta_index.mapping')
             )

        bro_cmd = ambari_format(
            'curl -s -XPOST http://{es_http_url}/_template/bro_index -d @{bro_index_path}')
        Execute(bro_cmd, logoutput=True)
        snort_cmd = ambari_format(
            'curl -s -XPOST http://{es_http_url}/_template/snort_index -d @{snort_index_path}')
        Execute(snort_cmd, logoutput=True)
        yaf_cmd = ambari_format(
            'curl -s -XPOST http://{es_http_url}/_template/yaf_index -d @{yaf_index_path}')
        Execute(yaf_cmd, logoutput=True)
        error_cmd = ambari_format(
            'curl -s -XPOST http://{es_http_url}/_template/error_index -d @{error_index_path}')
        Execute(error_cmd, logoutput=True)
        error_cmd = ambari_format(
            'curl -s -XPOST http://{es_http_url}/metaalerts -d @{meta_index_path}')
        Execute(error_cmd, logoutput=True)

    def elasticsearch_template_delete(self, env):
        import params
        env.set_params(params)

        bro_cmd = ambari_format('curl -s -XDELETE "http://{es_http_url}/bro_index*"')
        Execute(bro_cmd, logoutput=True)
        snort_cmd = ambari_format('curl -s -XDELETE "http://{es_http_url}/snort_index*"')
        Execute(snort_cmd, logoutput=True)
        yaf_cmd = ambari_format('curl -s -XDELETE "http://{es_http_url}/yaf_index*"')
        Execute(yaf_cmd, logoutput=True)
        error_cmd = ambari_format('curl -s -XDELETE "http://{es_http_url}/error_index*"')
        Execute(error_cmd, logoutput=True)

    def zeppelin_notebook_import(self, env):
        import params
        env.set_params(params)

        Logger.info(ambari_format('Searching for Zeppelin Notebooks in {metron_config_zeppelin_path}'))
        for dirName, subdirList, files in os.walk(params.metron_config_zeppelin_path):
            for fileName in files:
                if fileName.endswith(".json"):
                    zeppelin_cmd = ambari_format(
                        'curl -s -XPOST http://{zeppelin_server_url}/api/notebook/import -d "@' + os.path.join(dirName, fileName) + '"')
                    Execute(zeppelin_cmd, logoutput=True)

if __name__ == "__main__":
    Indexing().execute()
