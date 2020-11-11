import os
from argparse import ArgumentParser
import time
from datetime import timedelta, datetime, timezone
import delete_stack
import create_stack
import create_dashboard
from dotenv import load_dotenv
from aws_secrets import get_secret_value

# Stacks are deleted duration + offset seconds after creation; should be set to 900.
DELETE_TIME_OFFSET = 900
# Interval between "time elapsed" messages sent to user; should be set to 600.
MESSAGE_INTERVAL = 600


class Config(object):
    # Load configuration
    load_dotenv(dotenv_path="./config.env")
    try:
        aws_profile_name = os.getenv("AWS_PROFILE_NAME")
        region = os.getenv("REGION")
        total_users = int(os.getenv("TOTAL_USERS"))
        users_per_instance = int(os.getenv("USERS_PER_INSTANCE"))
        duration = os.getenv("DURATION")
        file_list = os.getenv("FILE_LIST")
        minio_url = os.getenv("MINIO_URL")
        minio_access_key = os.getenv("MINIO_ACCESS_KEY")
        minio_secret_key = os.getenv("MINIO_SECRET_KEY")
        minio_input_bucket = os.getenv("MINIO_INPUT_BUCKET")
        minio_output_bucket = os.getenv("MINIO_OUTPUT_BUCKET")
        influxdb_url = os.getenv("INFLUXDB_URL")
        prefix = os.getenv("PREFIX")
        icap_server = os.getenv("ICAP_SERVER")
        grafana_key = os.getenv("GRAFANA_KEY")
        grafana_file = os.getenv("GRAFANA_FILE")
        grafana_secret_id = os.getenv("GRAFANA_SECRET_ID")
        exclude_dashboard = os.getenv("EXCLUDE_DASHBOARD")
        preserve_stack = os.getenv("PRESERVE_STACK")
    except Exception as e:
        print(
            "Please create config.env file similar to config.env.sample or set environment variables for all variables in config.env.sample file")
        print(str(e))
        raise


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

    parser.add_argument('--file_list', '-l', default=Config.file_list,
                        help='Path to file list')

    parser.add_argument('--minio_url', '-m', default=Config.minio_url,
                        help='Minio URL (default: "http://minio.minio.svc.cluster.local:9000")')

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

    parser.add_argument('--prefix', '-p', default=Config.prefix,
                        help='Prefix for stack name (default: "")')

    parser.add_argument('--icap_server', '-v', default=Config.icap_server,
                        help='ICAP server endpoint URL (default: icap02.glasswall-icap.com)')

    parser.add_argument('--grafana_key', '-k',
                        type=str,
                        help='API key to be used for dashboard creation in grafana database',
                        default=Config.grafana_key)

    parser.add_argument('--grafana_file', '-f',
                        type=str,
                        help='path to grafana template used for dashboard creation',
                        default=Config.grafana_file)

    parser.add_argument('--grafana_secret_id', '-gsid', default=Config.grafana_secret_id,
                        help='The secret ID for the Grafana API Key stored in AWS Secrets')

    parser.add_argument('--exclude_dashboard', '-ed', action='store_true',
                        help='Setting this option will prevent the creation of a new dashboard for this stack')

    parser.add_argument('--preserve_stack', '-ps', action='store_true',
                        help='Setting this option will prevent the created stack from being automatically deleted.')

    return parser.parse_args()


# Starts the process of calling delete_stack after duration. Starts timer and displays messages updating users on status
def __start_delete_stack(additional_delay, config):
    duration = config.duration
    total_wait_time = additional_delay + int(duration)
    minutes = total_wait_time / 60
    finish_time = datetime.now(timezone.utc) + timedelta(seconds=total_wait_time)
    start_time = datetime.now(timezone.utc)

    print("Stack will be deleted after {0:.1f} minutes".format(minutes))

    while datetime.now(timezone.utc) < finish_time:
        if datetime.now(timezone.utc) != start_time:
            diff = datetime.now(timezone.utc) - start_time
            print("{0:.1f} minutes have elapsed, stack will be deleted in {1:.1f} minutes".format(diff.seconds / 60, (
                    total_wait_time - diff.seconds) / 60))
        time.sleep(MESSAGE_INTERVAL)

    delete_stack.Main.main(argv=None)


# creates a list of args to be passed to create_stack from Config (i.e. config.env or command line args)
def get_create_stack_args_list(config):
    # options to look out for when using create_stack, used to exclude all other unrelated options in config
    options = ["total_users", "users_per_instance", "duration", "list", "minio_url", "minio_access_key",
               "minio_secret_key", "minio_input_bucket", "minio_output_bucket", "influxdb_url", "prefix", "icap_server"]

    # go through Config object, compile list of relevant arguments
    args_list = []
    for key in config.__dict__:
        if not key.startswith('__') and key in options:
            if config.__dict__[key]:
                args_list.append('--{0}'.format(key))
                args_list.append(config.__dict__[key])

    return args_list


def main(config):
    args_list = get_create_stack_args_list(config)
    print("Creating Load Generators...")
    create_stack.Main.main(args_list)

    if config.exclude_dashboard:
        print("Dashboard will not be created")
    else:
        print("Creating dashboard...")
        create_dashboard.main(config)

    if config.preserve_stack:
        print("Stack will not be automatically deleted.")
    else:
        __start_delete_stack(DELETE_TIME_OFFSET, config)


if __name__ == "__main__":
    args = __get_commandline_args()

    # Get all argument values from Config.env file. Any command line args input manually will override config.env args.
    Config.total_users = int(args.total_users)
    Config.users_per_instance = int(args.users_per_instance)
    Config.users_per_instance = args.users_per_instance
    Config.duration = args.duration
    Config.file_list = args.file_list
    Config.minio_url = args.minio_url
    Config.minio_access_key = args.minio_access_key
    Config.minio_input_bucket = args.minio_input_bucket
    Config.minio_output_bucket = args.minio_output_bucket
    Config.influxdb_url = args.influxdb_url
    Config.prefix = args.prefix
    Config.icap_server = args.icap_server
    Config.grafana_file = args.grafana_file
    Config.grafana_key = args.grafana_key
    Config.grafana_secret_id = args.grafana_secret_id

    # these are flag/boolean arguments
    if args.exclude_dashboard:
        Config.exclude_dashboard = True
    elif Config.exclude_dashboard:
        Config.exclude_dashboard = int(Config.exclude_dashboard) == 1

    if args.preserve_stack:
        Config.preserve_stack = True
    elif Config.preserve_stack:
        Config.preserve_stack = int(Config.preserve_stack) == 1

    # Use Grafana key obtained either from config.env or from AWS secrets. Key from config.env gets priority.
    if not Config.grafana_key and not Config.grafana_secret_id:
        print("Must input either grafana_key or grafana_secret_id in config.env or using args")
        exit(0)
    elif not Config.grafana_key and not Config.exclude_dashboard:
        secret_response = get_secret_value(config=Config, secret_id=Config.grafana_secret_id)
        secret_val = next(iter(secret_response.values()))
        Config.grafana_key = secret_val
        if secret_val:
            print("Grafana secret key retrieved.")

    main(Config)
