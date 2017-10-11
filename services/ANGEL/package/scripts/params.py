from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.constants import Direction

config = Script.get_config()
stack_root = '/opt'

install_dir = config['configurations']['angel-env']['install_dir']
download_url = config['configurations']['angel-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

# upgrade params
stack_name = default("/hostLevelParams/stack_name", None)
upgrade_direction = default("/commandParams/upgrade_direction", Direction.UPGRADE)
stack_version_unformatted = config['hostLevelParams']['stack_version']

angel_conf_dir = default("/configurations/angel-env/angel_conf_dir", '/etc/angel')
angel_user = 'angel'
angel_group = 'angel'
if 'angel-env' in config['configurations'] and 'angel_user' in config['configurations']['angel-env']:
    angel_user = config['configurations']['angel-env']['angel_user']

# New Cluster Stack Version that is defined during the RESTART of a Stack Upgrade
version = default("/commandParams/version", None)

user_group = config['configurations']['cluster-env']['user_group']
proxyuser_group = config['configurations']['hadoop-env']['proxyuser_group']

security_enabled = config['configurations']['cluster-env']['security_enabled']
if security_enabled:
    _hostname_lowercase = config['hostname'].lower()
    angel_jaas_princ = config['configurations']['angel-env']['angel_principal_name']
    angel_keytab_path = config['configurations']['angel-env']['angel_keytab_path']

angel_bin_dir = install_dir + '/bin'

java_home = config['hostLevelParams']['java_home']
angel_log_dir = config['configurations']['angel-env']['angel_log_dir']
angel_run_dir = config['configurations']['angel-env']['angel_run_dir']
ambari_state_file = format("{angel_run_dir}/ambari-state.txt")

if (('angel-conf' in config['configurations']) and ('content' in config['configurations']['angel-conf'])):
    angel_conf_content = config['configurations']['angel-conf']['content']
else:
    angel_conf_content = None

if (('angel-log4j' in config['configurations']) and ('content' in config['configurations']['angel-log4j'])):
    angel_log4j_content = config['configurations']['angel-log4j']['content']
else:
    angel_log4j_content = None

angel_env_sh_template = config['configurations']['angel-env']['content']

hostname = config['hostname']

cluster_name = config["clusterName"]
# Cluster Zookeeper quorum
zookeeper_quorum = None
if not len(default("/clusterHostInfo/zookeeper_hosts", [])) == 0:
    if 'zoo.cfg' in config['configurations'] and 'clientPort' in config['configurations']['zoo.cfg']:
        zookeeper_clientPort = config['configurations']['zoo.cfg']['clientPort']
    else:
        zookeeper_clientPort = '2181'
    zookeeper_quorum = (':' + zookeeper_clientPort + ',').join(config['clusterHostInfo']['zookeeper_hosts'])
    # last port config
    zookeeper_quorum += ':' + zookeeper_clientPort

# smokeuser
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env']['smokeuser_principal_name']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
