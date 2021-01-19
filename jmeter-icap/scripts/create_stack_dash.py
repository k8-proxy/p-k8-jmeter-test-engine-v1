import os
from argparse import ArgumentParser
from datetime import timedelta, datetime, timezone
import delete_stack
import create_stack
import create_dashboard
from aws_secrets import get_secret_value
from threading import Thread
from time import sleep
from database_ops import database_insert_test
from config_params import Config

import uuid

# Stacks are deleted duration + offset seconds after creation; should be set to 900.
DELETE_TIME_OFFSET = 900

# Interval for how often "time elapsed" messages are displayed for delete stack process
MESSAGE_INTERVAL = 600


# set all possible arguments/options that can be input into the script
def __get_commandline_args():
    parser = ArgumentParser(fromfile_prefix_chars='@',
                            description='Creates k8 stack, generates Grafana Dashboard, deletes stack when complete')

    parser.add_argument('--total_users', '-t', default=Config.total_users,
                        help='total number of users in the test (default: 100)')

    parser.add_argument('--users_per_instance', '-u', default=Config.users_per_instance,
                        help='number of users per instance (default: 25)')

    parser.add_argument('--duration', '-d', default=Config.duration,
                        help='duration of test (default: 60)')

    parser.add_argument('--test_data_file', '-l', default=Config.list,
                        help='Path to file list')

    parser.add_argument('--minio_url', '-m', default=Config.minio_url,
                        help='Minio URL (default: "http://minio.minio.svc.cluster.local:9000")')

    parser.add_argument('--minio_external_url', '-me', default=Config.minio_external_url,
                        help='Minio URL (default: "http://localhost:9000")')

    parser.add_argument('--minio_access_key', '-a', default=Config.minio_access_key,
                        help='Minio access key')

    parser.add_argument('--minio_secret_key', '-s', default=Config.minio_secret_key,
                        help='Minio secret key')

    parser.add_argument('--minio_input_bucket', '-i', default=Config.minio_input_bucket,
                        help='Minio input bucket name (default: "input")')

    parser.add_argument('--minio_output_bucket', '-o', default=Config.minio_output_bucket,
                        help='Minio output bucket name (default: "output")')

    parser.add_argument('--influxdb_url', '-x', default=Config.influxdb_url,
                        help='Influx DB URL (default: "influxdb.influxdb.svc.cluster.local")')

    parser.add_argument('--influx_host', '-ih', default=Config.influx_host,
                        help=f'Influx DB host (default: {Config.influx_host})')

    parser.add_argument('--prefix', '-p', default=Config.prefix,
                        help='Prefix for stack name (default: "")')

    parser.add_argument('--icap_server_url', '-v', default=Config.icap_server,
                        help='ICAP server endpoint URL (default: icap02.glasswall-icap.com)')

    parser.add_argument('--grafana_url', '-gu',
                        type=str,
                        help='URL to Grafana instance',
                        default=Config.grafana_url)

    parser.add_argument('--grafana_api_key', '-k',
                        type=str,
                        help='API key to be used for dashboard creation in grafana database',
                        default=Config.grafana_api_key)

    parser.add_argument('--grafana_file', '-f',
                        type=str,
                        help='path to grafana template used for dashboard creation',
                        default=Config.grafana_file)

    parser.add_argument('--grafana_secret', '-gs', default=Config.grafana_secret,
                        help='The secret ID for the Grafana API Key stored in AWS Secrets')

    parser.add_argument('--exclude_dashboard', '-ed', action='store_true',
                        help='Setting this option will prevent the creation of a new dashboard for this stack')

    parser.add_argument('--preserve_stack', '-ps', action='store_true',
                        help='Setting this option will prevent the created stack from being automatically deleted.')

    parser.add_argument('--icap_server_port', '-port', default=Config.icap_server_port,
                        help='Port of ICAP server used for testing')

    parser.add_argument('--tls_verification_method', '-tls', default=Config.tls_verification_method,
                        help='Verification method used with TLS')

    parser.add_argument('--enable_tls', '-et', default=Config.enable_tls,
                        help='Whether or not to enable TLS')

    parser.add_argument('--jmx_file_path', '-jmx', default=Config.jmx_file_path,
                        help='The file path of the JMX file under the test')

    parser.add_argument('--proxy_static_ip', '-proxy', default=Config.proxy_static_ip,
                        help='Static IP for when proxy is used')

    parser.add_argument('--store_results', '-sr', action='store_true',
                        help='Setting this option will cause all test runs to be recorded into influxdb')

    parser.add_argument('--load_type', '-load', default=Config.load_type,
                        help='Load type: Direct or Proxy')

    parser.add_argument('--grafana_username', '-un', default=Config.grafana_username,
                        help='Load type: Direct or Proxy')

    parser.add_argument('--grafana_password', '-pw', default=Config.grafana_password,
                        help='Load type: Direct or Proxy')

    return parser.parse_args()


# Starts the process of calling delete_stack after duration. Starts timer and displays messages updating users on status
def __start_delete_stack(config, additional_delay):
    delete_stack_args = ["--prefix", config.prefix]
    total_wait_time = additional_delay + int(config.duration)
    minutes = total_wait_time / 60
    finish_time = datetime.now(timezone.utc) + timedelta(seconds=total_wait_time)
    start_time = datetime.now(timezone.utc)

    print("Stack will be deleted after {0:.1f} minutes".format(minutes))

    while datetime.now(timezone.utc) < finish_time:
        if datetime.now(timezone.utc) != start_time and datetime.now(timezone.utc) + timedelta(seconds=MESSAGE_INTERVAL) < finish_time:
            diff = datetime.now(timezone.utc) - start_time
            print("{0:.1f} minutes have elapsed, stack will be deleted in {1:.1f} minutes".format(diff.seconds / 60, (
                    total_wait_time - diff.seconds) / 60))
            sleep(MESSAGE_INTERVAL)

    print("Deleting stack with prefix: {0}".format(config.prefix))
    delete_stack.Main.main(argv=delete_stack_args)


# creates a list of args to be passed to create_stack from Config (i.e. config.env or command line args)
def get_args_list(config, options):
    # go through Config object, compile list of relevant arguments
    args_list = []
    for key in config.__dict__:
        if not key.startswith('__') and key in options:
            if config.__dict__[key]:
                args_list.append('--{0}'.format(key))
                args_list.append(str(config.__dict__[key]))

    return args_list


def run_using_ui(ui_json_params):
    ui_config = Config
    additional_delay = 0
    # Set Config values gotten from front end
    if ui_json_params['total_users']:
        ui_config.total_users = ui_json_params['total_users']
    if ui_json_params['ramp_up_time']:
        ui_config.ramp_up_time = ui_json_params['ramp_up_time']
    if ui_json_params['duration']:
        ui_config.duration = ui_json_params['duration']
    if ui_json_params['prefix']:
        ui_config.prefix = ui_json_params['prefix']
    if ui_json_params['icap_endpoint_url']:

        if ui_json_params['load_type'] == "Direct":
            ui_config.load_type = 'Direct'
            ui_config.icap_server = ui_json_params['icap_endpoint_url']
        elif ui_json_params['load_type'] == "Proxy Offline":
            # this comes as "icap_endpoint_url" from front end, but may also represent proxy IP if proxy load selected
            ui_config.load_type = 'Proxy'
            ui_config.proxy_static_ip = ui_json_params['icap_endpoint_url']
        elif ui_json_params['load_type'] == "Proxy SharePoint":
            ui_config.load_type = 'SharePoint'
            sharepoint_field_input = str(ui_json_params['icap_endpoint_url'])
            (sharepoint_ip, sharepoint_hosts) = sharepoint_field_input.split(maxsplit=1)
            ui_config.sharepoint_ip = sharepoint_ip
            ui_config.sharepoint_host_names = sharepoint_hosts

    __ui_set_files_for_load_type(ui_config)

    # If Grafana API key provided, that takes precedence. Otherwise get key from AWS. If neither method provided, error output.
    handle_grafana_authentication(ui_config)

    # ensure that preserve stack and create_dashboard are at default values
    ui_config.preserve_stack = False
    ui_config.exclude_dashboard = False

    __ui_set_tls_and_port_params(ui_config, ui_json_params['load_type'], ui_json_params['enable_tls'],
                                 ui_json_params['tls_ignore_error'], ui_json_params['port'])

    dashboard_url, grafana_uid = main(ui_config, additional_delay, True)

    if bool(int(ui_config.store_results)):
        results_analysis_thread = Thread(target=store_and_analyze_after_duration, args=(ui_config, grafana_uid, additional_delay))
        results_analysis_thread.start()

    return dashboard_url

def store_and_analyze_after_duration(config, grafana_uid, additional_delay):
    start_time = str(datetime.now())
    sleep(additional_delay + int(config.duration))
    run_id = uuid.uuid4()
    print("test completed, storing results to the database")
    final_time = str(datetime.now())
    database_insert_test(config, run_id, grafana_uid, start_time, final_time)

def stop_tests_using_ui(prefix=''):

    if prefix == '':
        delete_stack.Main.main(argv=[])
    else:
        delete_stack_options = ["--prefix", prefix]
        delete_stack.Main.main(argv=delete_stack_options)


def __ui_set_tls_and_port_params(config, input_load_type, input_enable_tls, input_tls_ignore_verification, input_port):
    if input_load_type == "Direct":

        # enable/disable tls based on user input
        config.enable_tls = str(input_enable_tls)

        # if user entered a port, use that. Otherwise port will be set depending on tls_enabled below.
        if input_port:
            config.icap_server_port = input_port

        # if user did not provide port, set one depending on whether or not tls is enabled
        if not input_port:
            if input_enable_tls:
                config.icap_server_port = "443"
            else:
                config.icap_server_port = "1344"

        # If TLS is enabled, get the user preference as to whether or not TLS verification should be used
        if input_enable_tls:
            config.tls_verification_method = "tls-no-verify" if input_tls_ignore_verification else ""


def __ui_set_files_for_load_type(config):
    if config.load_type == "Direct":
        config.jmx_file_path = './ICAP-Direct-File-Processing/ICAP_Direct_FileProcessing_k8_v3.jmx'
        config.grafana_file = './ICAP-Direct-File-Processing/k8-test-engine-dashboard.json'
        config.list = './ICAP-Direct-File-Processing/gov_uk_files.csv'

    elif config.load_type == "Proxy":
        config.jmx_file_path = './ICAP-Proxy-Site/ProxySite_Processing_v1.jmx'
        config.grafana_file = './ICAP-Proxy-Site/ProxySite_Dashboard_Template.json'
        config.list = './ICAP-Proxy-Site/proxyfiles.csv'

    elif config.load_type == "SharePoint":
        config.jmx_file_path = './ICAP-Sharepoint-Site/ICAP-Sharepoint-Upload-Download-v1.jmx'
        config.grafana_file = './ICAP-Sharepoint-Site/Sharepoint-Demo-Dashboard.json'
        config.list = './ICAP-Sharepoint-Site/sharepoint_files.csv'


def main(config, additional_delay, ui_run = False):
    dashboard_url = ''
    grafana_uid = ''

    # options to look out for when using create_stack, used to exclude all other unrelated options in config
    #create_stack_options = ["total_users", "users_per_instance", "duration", "list", "minio_url", "minio_external_url", "minio_access_key",
    #           "minio_secret_key", "minio_input_bucket", "minio_output_bucket", "influxdb_url", "prefix", "icap_server",
    #           "icap_server_port", "enable_tls", "tls_verification_method", "jmx_file_path", "proxy_static_ip", "load_type"]

    #create_stack_args = get_args_list(config, create_stack_options)

    print("Creating Load Generators...")
    create_stack.Main.main(config)

    if config.preserve_stack:
        print("Stack will not be automatically deleted.")
    else:
        delete_stack_thread = Thread(target=__start_delete_stack, args=(config, additional_delay))
        delete_stack_thread.start()

    if config.exclude_dashboard:
        print("Dashboard will not be created")
    else:
        print("Creating dashboard...")
        dashboard_url, grafana_uid = create_dashboard.main(config)

    if not ui_run and config.store_results:
        print('Starting the analyzer thread')
        analyzer_thread = Thread(target=store_and_analyze_after_duration, args=(config, grafana_uid, additional_delay))
        analyzer_thread.start()

    return dashboard_url, grafana_uid


def handle_grafana_authentication(config):

    # Use Grafana key obtained either from config.env or from AWS secrets, or use username/password. Key from config.env/AWS gets priority.
    if not config.grafana_api_key and not config.grafana_secret and not (config.grafana_username and config.grafana_password):
        print("Must input either grafana_api_key, grafana_secret, or username/password in config.env or using args")
        exit(0)
    elif not config.grafana_api_key and not config.exclude_dashboard and not (
            config.grafana_username and config.grafana_password):
        secret_response = get_secret_value(config=config, secret_id=config.grafana_secret)
        secret_val = next(iter(secret_response.values()))
        config.grafana_api_key = secret_val
        if secret_val:
            print("Grafana secret key retrieved.")


if __name__ == "__main__":
    args = __get_commandline_args()

    # Get all argument values from Config.env file. Any command line args input manually will override config.env args.
    Config.total_users = int(args.total_users)
    Config.users_per_instance = args.users_per_instance
    Config.duration = args.duration
    Config.list = args.test_data_file
    Config.minio_url = args.minio_url
    Config.minio_access_key = args.minio_access_key
    Config.minio_input_bucket = args.minio_input_bucket
    Config.minio_output_bucket = args.minio_output_bucket
    Config.influxdb_url = args.influxdb_url
    Config.influx_host = args.influx_host
    Config.prefix = args.prefix
    Config.icap_server = args.icap_server_url
    Config.grafana_url = args.grafana_url
    Config.grafana_file = args.grafana_file
    Config.grafana_api_key = args.grafana_api_key
    Config.grafana_secret = args.grafana_secret
    Config.icap_server_port = args.icap_server_port
    Config.tls_verification_method = args.tls_verification_method
    Config.proxy_static_ip = args.proxy_static_ip
    Config.load_type = args.load_type
    Config.grafana_username = args.grafana_username
    Config.grafana_password = args.grafana_password

    # these are flag/boolean arguments
    if args.exclude_dashboard:
        Config.exclude_dashboard = True
    elif Config.exclude_dashboard:
        Config.exclude_dashboard = int(Config.exclude_dashboard) == 1

    if args.preserve_stack:
        Config.preserve_stack = True
    elif Config.preserve_stack:
        Config.preserve_stack = int(Config.preserve_stack) == 1

    if args.store_results:
        Config.store_results = True
    elif Config.store_results:
        Config.store_results = int(Config.store_results) == 1

    handle_grafana_authentication(Config)
    Config.enable_tls = (int(args.enable_tls) == 1)
    Config.jmx_file_path = args.jmx_file_path

    main(Config, DELETE_TIME_OFFSET)
