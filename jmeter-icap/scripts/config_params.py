import os
from dotenv import load_dotenv

class Config(object):
    # Load configuration
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, 'config.env'), override=True)
    try:
        # these field names should not be changed as they correspond exactly to the names of create_stack's params.
        aws_profile_name = os.getenv("AWS_PROFILE_NAME")
        region = os.getenv("REGION")
        total_users = int(os.getenv("TOTAL_USERS"))
        users_per_instance = int(os.getenv("USERS_PER_INSTANCE"))
        duration = os.getenv("DURATION")
        list = os.getenv("TEST_DATA_FILE")
        minio_url = os.getenv("MINIO_URL")
        minio_external_url = os.getenv("MINIO_EXTERNAL_URL")
        minio_access_key = os.getenv("MINIO_ACCESS_KEY")
        minio_secret_key = os.getenv("MINIO_SECRET_KEY")
        minio_input_bucket = os.getenv("MINIO_INPUT_BUCKET")
        minio_output_bucket = os.getenv("MINIO_OUTPUT_BUCKET")
        influxdb_url = os.getenv("INFLUXDB_URL")
        influx_host = os.getenv("INFLUX_HOST",'localhost')
        influx_port = os.getenv("INFLUX_PORT", 8086)
        prefix = os.getenv("PREFIX")
        icap_server = os.getenv("ICAP_SERVER_URL")
        icap_endpoint_url = os.getenv("ICAP_SERVER_URL")
        grafana_url = os.getenv("GRAFANA_URL")
        grafana_api_key = os.getenv("GRAFANA_API_KEY")
        grafana_file = os.getenv("GRAFANA_FILE")
        grafana_secret = os.getenv("GRAFANA_SECRET")
        exclude_dashboard = os.getenv("EXCLUDE_DASHBOARD")
        preserve_stack = os.getenv("PRESERVE_STACK")
        icap_server_port = os.getenv("ICAP_SERVER_PORT")
        enable_tls = os.getenv("ENABLE_TLS")
        store_results = True
        jmx_file_path = os.getenv("JMX_FILE_PATH")
        tls_verification_method = os.getenv("TLS_VERIFICATION_METHOD")
        proxy_static_ip = os.getenv("PROXY_STATIC_IP")
        load_type = os.getenv("LOAD_TYPE")
        grafana_username = os.getenv("GRAFANA_USERNAME")
        grafana_password = os.getenv("GRAFANA_PASSWORD")
    except Exception as e:
        print(
            "Please create config.env file similar to config.env.sample or set environment variables for all variables in config.env.sample file")
        print(str(e))
        raise