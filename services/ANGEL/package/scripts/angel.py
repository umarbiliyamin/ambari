import glob
import \
    ambari_simplejson as json  # simplejson is much faster comparing to Python 2.6 json module and has the same functions set.
import os
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core.exceptions import Fail
from resource_management.core import shell
from resource_management.core.source import Template, InlineTemplate
from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.resources.system import Execute
from resource_management.libraries.providers.hdfs_resource import HdfsResourceProvider
from resource_management import is_empty
from resource_management.libraries.functions.decorator import retry
from resource_management.core.logger import Logger


def install_angel():
    import params
    Directory(
        [params.angel_conf_dir],
        owner=params.angel_user,
        group=params.angel_group,
        mode=0775,
        create_parents=True)
    if not os.path.exists('/opt/' + params.version_dir) or not os.path.exists(params.install_dir):
        Execute('rm -rf %s' %  '/opt/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.angel_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C /opt')
        Execute('ln -s /opt/' + params.version_dir + ' ' + params.install_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.angel_conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute("echo 'export PATH=%s/bin:$PATH'>>/etc/profile.d/hadoop.sh" %
                params.install_dir)
        Execute('chown -R %s:%s /opt/%s' %
                (params.angel_user, params.angel_group, params.version_dir))
        Execute('chown -R %s:%s %s' %
                (params.angel_user, params.angel_group, params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)

class Angel(Script):
    def get_component_name(self):
        return "angel"

    def pre_upgrade_restart(self, env, upgrade_type=None):
        print 'todo'

    def install(self, env):
        import params
        env.set_params(params)
        install_angel()

    def configure(self, env, upgrade_type=None):
        import params
        env.set_params(params)

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.pid_file)

if __name__ == "__main__":
    Angel().execute()

