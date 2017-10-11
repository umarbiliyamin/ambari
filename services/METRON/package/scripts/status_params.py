#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions import default, format
from resource_management.libraries.functions.version import format_stack_version

config = Script.get_config()

metron_user = config['configurations']['metron-env']['metron_user']
metron_home = config['configurations']['metron-env']['install_dir']
metron_zookeeper_config_dir = config['configurations']['metron-env']['metron_zookeeper_config_dir']
metron_zookeeper_config_path = format('{metron_home}/{metron_zookeeper_config_dir}')
# indicates if zk_load_configs.sh --mode PUSH has been executed
zk_configured_flag_file = metron_zookeeper_config_path + '/../metron_zookeeper_configured'

# Parsers
parsers = config['configurations']['metron-parsers-env']['parsers']
parsers_configured_flag_file = metron_zookeeper_config_path + '/../metron_parsers_configured'
parsers_acl_configured_flag_file = metron_zookeeper_config_path + '/../metron_parsers_acl_configured'
rest_acl_configured_flag_file = metron_zookeeper_config_path + '/../metron_rest_acl_configured'

# Enrichment
metron_enrichment_topology = 'enrichment'
enrichment_input_topic = config['configurations']['metron-enrichment-env']['enrichment_input_topic']
enrichment_kafka_configured_flag_file = metron_zookeeper_config_path + '/../metron_enrichment_kafka_configured'
enrichment_kafka_acl_configured_flag_file = metron_zookeeper_config_path + '/../metron_enrichment_kafka_acl_configured'
enrichment_hbase_configured_flag_file = metron_zookeeper_config_path + '/../metron_enrichment_hbase_configured'
enrichment_hbase_acl_configured_flag_file = metron_zookeeper_config_path + '/../metron_enrichment_hbase_acl_configured'
enrichment_geo_configured_flag_file = metron_zookeeper_config_path + '/../metron_enrichment_geo_configured'

enrichment_hbase_table = config['configurations']['metron-enrichment-env']['enrichment_hbase_table']
enrichment_hbase_cf = config['configurations']['metron-enrichment-env']['enrichment_hbase_cf']
threatintel_hbase_table = config['configurations']['metron-enrichment-env']['threatintel_hbase_table']
threatintel_hbase_cf = config['configurations']['metron-enrichment-env']['threatintel_hbase_cf']
update_hbase_table = config['configurations']['metron-indexing-env']['update_hbase_table']
update_hbase_cf = config['configurations']['metron-indexing-env']['update_hbase_cf']

# Profiler
metron_profiler_topology = 'profiler'
profiler_input_topic = config['configurations']['metron-enrichment-env']['enrichment_output_topic']
profiler_hbase_table = config['configurations']['metron-profiler-env']['profiler_hbase_table']
profiler_hbase_cf = config['configurations']['metron-profiler-env']['profiler_hbase_cf']
profiler_configured_flag_file = metron_zookeeper_config_path + '/../metron_profiler_configured'
profiler_acl_configured_flag_file = metron_zookeeper_config_path + '/../metron_profiler_acl_configured'
profiler_hbase_configured_flag_file = metron_zookeeper_config_path + '/../metron_profiler_hbase_configured'
profiler_hbase_acl_configured_flag_file = metron_zookeeper_config_path + '/../metron_profiler_hbase_acl_configured'


# Indexing
metron_indexing_topology = 'indexing'
indexing_input_topic = config['configurations']['metron-indexing-env']['indexing_input_topic']
indexing_configured_flag_file = metron_zookeeper_config_path + '/../metron_indexing_configured'
indexing_acl_configured_flag_file = metron_zookeeper_config_path + '/../metron_indexing_acl_configured'
indexing_hdfs_perm_configured_flag_file = metron_zookeeper_config_path + '/../metron_indexing_hdfs_perm_configured'
indexing_hbase_configured_flag_file = metron_zookeeper_config_path + '/../metron_indexing_hbase_configured'
indexing_hbase_acl_configured_flag_file = metron_zookeeper_config_path + '/../metron_indexing_hbase_acl_configured'

# REST
metron_rest_port = config['configurations']['metron-rest-env']['metron_rest_port']

# UI
metron_management_ui_port = config['configurations']['metron-management-ui-env']['metron_management_ui_port']

# Storm
storm_rest_addr = config['configurations']['metron-env']['storm_rest_addr']

# Zeppelin
zeppelin_server_url = config['configurations']['metron-env']['zeppelin_server_url']

# Security
stack_version_unformatted = str(config['hostLevelParams']['stack_version'])
stack_version_formatted = format_stack_version(stack_version_unformatted)
hostname = config['hostname']
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))
tmp_dir = Script.get_tmp_dir()

metron_principal_name = config['configurations']['metron-env']['metron_principal_name']
metron_keytab_path = config['configurations']['metron-env']['metron_service_keytab']
