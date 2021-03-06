from resource_management.core.resources import Execute
from resource_management.libraries.functions import format

RESULT_CODE_OK = 'OK'
RESULT_CODE_CRITICAL = 'CRITICAL'
RESULT_CODE_UNKNOWN = 'UNKNOWN'
STACK_ROOT = '{{cluster-env/stack_root}}'
TITAN_RUN_DIR = 'titan.run.dir'
TITAN_USER = 'titan.user'


def execute(configurations={}, parameters={}, host_name=None):
    """
    Returns a tuple containing the result code and a pre-formatted result label

    Keyword arguments:
    configurations (dictionary): a mapping of configuration key to value
    parameters (dictionary): a mapping of script parameter key to value
    host_name (string): the name of this host where the alert is running
    """
    titan_bin_dir = configurations[STACK_ROOT] + format("/current/titan-server/bin")

    gremlin_server_script_path = titan_bin_dir + format("/gremlin-server-script.sh")

    titan_pid_file = parameters[TITAN_RUN_DIR] + format("/titan.pid")
    titan_user = parameters[TITAN_USER]
    (code, msg) = get_check_result(gremlin_server_script_path, titan_pid_file, titan_user)
    return (code, msg)

def get_tokens():
    """
    Returns a tuple of tokens in the format {{site/property}} that will be used
    to build the dictionary passed into execute
    """
    return (STACK_ROOT, TITAN_RUN_DIR)


def get_check_result(gremlin_server_script_path, titan_pid_file, titan_user):
    cmd = format("{gremlin_server_script_path} status {titan_pid_file}")
    try:
        result = Execute(cmd,
                         user=titan_user
                         )
        return (RESULT_CODE_OK, ["titan server is up and running"])
    except Exception, ex:
        return (RESULT_CODE_CRITICAL, [ex])
