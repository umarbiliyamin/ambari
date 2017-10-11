#!/usr/bin/env python

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


def properties_inline_template(configurations):
    return InlineTemplate('''{% for key, value in configurations_dict.items() %}{{ key }}={{ value }}
{% endfor %}''', configurations_dict=configurations)


def properties_config(filename, configurations=None, conf_dir=None,
                      mode=None, owner=None, group=None, brokerid=None):
    config_content = properties_inline_template(configurations)
    File(format("{conf_dir}/{filename}"), content=config_content, owner=owner,
         group=group, mode=mode)
