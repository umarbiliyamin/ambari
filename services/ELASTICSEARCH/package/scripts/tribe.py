#!/usr/bin/env python
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.source import Template

def elastic():
    import params

    params.path_data = params.path_data.replace('"', '')
    data_path = params.path_data.replace(' ', '').split(',')
    data_path[:] = [x.replace('"', '') for x in data_path]

    directories = [params.log_dir, params.pid_dir, params.conf_dir]
    directories = directories + data_path + ["{0}/scripts".format(params.conf_dir)]

    Directory(directories,
              create_parents=True,
              mode=0755,
              owner=params.elastic_user,
              group=params.elastic_group
              )

    print "Master env: ""{0}/elastic-env.sh".format(params.conf_dir)
    File("{0}/elastic-env.sh".format(params.conf_dir),
         owner=params.elastic_user,
         group=params.elastic_group,
         content=InlineTemplate(params.elastic_env_sh_template)
         )

    configurations = params.config['configurations']['elastic-site']

    print "Master yml: ""{0}/elasticsearch.yml".format(params.conf_dir)
    File("{0}/elasticsearch.yml".format(params.conf_dir),
         content=Template(
             "elasticsearch.tribe.yaml.j2",
             configurations=configurations),
         owner=params.elastic_user,
         group=params.elastic_group
         )

    print "Master sysconfig: /etc/sysconfig/elasticsearch"
    File("/etc/sysconfig/elasticsearch",
         owner="root",
         group="root",
         content=InlineTemplate(params.sysconfig_template)
         )
