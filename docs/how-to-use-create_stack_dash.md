# Using create_stack_dash.py to Create Load Generators and Corresponding Dashboards


## Table of Contents
  * [Introduction](#introduction)
  * [Prerequisites](#prerequisites)
  * [Using config.env to pass parameters to create_stack_dash.py](#using-configenv-to-pass-parameters-to-create-stack-dashpy)
  * [Options available for the create_stack_dash.py script](#options-available-for-the-create-stack-dashpy-script)
  * [How create_stack_dash.py works](#how-create-stack-dashpy-works)
  * [Running the create_stack_dash.py script](#running-the-create-stack-dashpy-script)
  * [Troubleshooting](#troubleshooting)


## Introduction

This script launches a Cloudformation stack that spins up load generators. Then it creates Grafana Dashboards that display various metrics from the load generators.

## Prerequisites

1. Install [Python](https://www.python.org/downloads/).

2. Ensure boto3, requests and dotenv python packages are installed. This can be done using the following console commands:

```
pip install boto3
pip install requests
pip install python-dotenv
```

3. Set AWS authentication for the Cloudformation stack that will be created. This can be done by configuring AWS on the machine running the script using this script. Make sure AWS CLI is installed on the machine and that a user exists with an AWS access key (can be created under IAM, Security Credentials in the AWS console), then run the following commands:

```
aws configure
```

Prompts will appear asking for the following information:

```
AWS Access Key ID:
AWS Secret Access Key:
Default region name [eu-west-1]:
Default output format [None]:
```

Input the correct values; the last prompt can be left at default by pressing enter and skipping input.

Once configured, the AWS credentials and config files can be found in the AWS folder located in "~/.aws/" on linux systems or "%USERPROFILE%\\.aws" in Windows systems. At the top of the config folder a profile name in brackets should be present (ex: [default], here "default" will be the profile name to use in the config.env file discussed in the next step).

4. Update the config.env file with the AWS profile information.

Create config.env file by copying the existing config.env.sample file. Update the file with the following details:

- aws_profile_name - The AWS profile created in step 3.
- bucket - Bucket name where a file with number of instances will be created.

## Using config.env to pass parameters to create_stack_dash.py

The config.env file is the preferred way to pass parameters to this script, it should be located in the same folder as create_stack_dash. It contains many parameters that translate to options (listed in options section below) when running the script. Below is a sample config.env file:

```
AWS_PROFILE_NAME=default
REGION=eu-west-1
TOTAL_USERS=100
USERS_PER_INSTANCE=25
DURATION=1
FILE_LIST=
MINIO_URL=http://miniocluster.local:9000
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_INPUT_BUCKET=input
MINIO_OUTPUT_BUCKET=output
INFLUXDB_URL=http://influxdb.local:8086
PREFIX=demo
ICAP_SERVER=
GRAFANA_URL=
GRAFANA_KEY=
GRAFANA_FILE=grafana_template.json
EXCLUDE_DASHBOARD=0
PRESERVE_STACK=0
```

These parameters have corresponding options that can be used during script execution, they do not have to be set in config.env. Many of the parameters above are also optional, they can be omitted. Any options input manually via the command line will override options within the config.env file. For example, if the config.env file is set to allow dashboard creation:

```
EXCLUDE_DASHBOARD=0
```

But if the option to exclude dashboard creation is used:

```
python create_stack_dash.py -x
```
The Dashboard will still not be created (the option -x prevents dashboard creation) despite the content of the config.env file. The options below correspond to the same name parameters in the config.env file; they are listed along with brief descriptions of their usage.

## Options available for the create_stack_dash.py script

To see the available options for when running the script, use:
```
python create_stack_dash.py -h
```

Below is a table highlighting all the available options

<table>
<tr>
<td width="200"> Option </td> <td> Description </td>
</tr>
<tr>
<td> --total_users, -t </td>
<td>
Total number of users for the test, Default value is 4000.
</td>
</tr>
<tr>
<td> --users_per_instance, -u </td>
<td>
Number of users per instance (default: 25)
</td>
</tr>
<tr>
<td> --duration, -d </td>
<td>
Duration of the test, default value: 900 seconds
</td>
</tr>
<tr>
<td> --file_list, -l </td>
<td>
Path to list of file used for testing
</td>
</tr>
<tr>
<td> --minio_url, -m </td>
<td>
Minio URL
</td>
</tr>
<tr>
<td> --minio_access_key, -a </td>
<td>
Minio access key
</td>
</tr>
<tr>
<td> --minio_secret_key, -s </td>
<td>
Minio secret key
</td>
</tr>
<tr>
<td> --minio_input_bucket, -i </td>
<td>
Minio input bucket name
</td>
</tr>
<tr>
<td>--minio_output_bucket, -o </td>
<td>
Minio output bucket name
</td>
</tr>
<tr>
<td> --influxdb_url, -x </td>
<td>
URL to Influx Dataase
</td>
</tr>
<tr>
<td> --prefix, -p </td>
<td>
Prefix for stack name (default: "")
</td>
</tr>
<tr>
<td> --icap_server, -v </td>
<td>
ICAP server endpoint URL
</td>
</tr>
<tr>
<td> --grafana_url, -g </td>
<td>
The URL to the Grafana database's home page (typically this would be the "MachineIP:3000")
</td>
</tr>
<tr>
<td> --grafana_file, -f </td>
<td>
This takes the tag of the server containing the Grafana database; this server will automatically be started if it is stopped. Tags in AWS have both a key and a value. The key field should contain "Name", only the value of the tag is what should be provided to this option. The tag must have a value field; it should not be empty. (Note: The --grafana_url option will prevent this option from taking effect, as the Grafana server IP would be obtained directly from that).
</td>
</tr>
<tr>
<td>--grafana_secret_id, -gsid</td>
<td>
The secret name of the Grafana API Key inside AWS Secrets Manager. This will be used to retrieve the key for use when generating Grafana dashboards. (Note: The --grafana_key option will prevent this option from taking effect; a user directly providing a key would negate the need for a key lookup).
</td>
</tr>
<tr>
<td> --exclude_dashboard, -x </td>
<td>
This takes no arguments. If set (ex: create_stack_dash -x), a Grafana dashboard will not be created when the script is run.
</td>
</tr>
<tr>
<td> --preserve_stack, -s </td>
<td>
This takes no arguments. If set (ex: create_stack_dash -s), it will prevent the stack created from being automatically deleted after the duration period specified above is complete.
</td>
</tr>
</table>

## How create_stack_dash.py works

![how_create_stack_dash_works](pngs/create_stack_dash.png)

## Running the create_stack_dash.py script

To run the create_stack_dash.py script, use the following command:
```
python create_stack_dash.py
```

Followed by the options required. This can be done manually, as seen in this example:
```
python create_stack_dash.py -f "grafana_template.json" -k "grafana key" -g "link to grafana home page" -p "test-prefix"
```
Or the Config.env file would contain all the parameters required.

A successful run should output information on number of users, duration, and links to the end point and Grafana dashboard. See example below:
```
Creating Load Generators...
Deploying 1 instances in the ASG by creating test-prefix-aws-jmeter-test-engine-2020-11-03-01-39 cloudformation stack
Stack created with the following properties:
Total Users: 4000
Duration: 900
Endpoint URL: icap-client.uksouth.cloudapp.azure.com
Creating dashboard...
Dashboard created at:
http://64.159.132.71:3000//d/LVI8JIhMk/test-prefix-icap-live-performance-dashboard
Stack will be deleted after 45 minutes
10.0 minutes have elapsed, stack will be deleted in 35.0 minutes
20.0 minutes have elapsed, stack will be deleted in 25.0 minutes
30.0 minutes have elapsed, stack will be deleted in 15.0 minutes
40.0 minutes have elapsed, stack will be deleted in 5.0 minutes
deleting stack named: test-prefix-aws-jmeter-test-engine-2020-11-03-01-39
```

## Troubleshooting

Below is a list of potential issues end users might face along with some suggested solutions:

### Grafana Dashboard is not being created
- Check that the "exclude_dashboard" option is not enabled
- The grafana_key or grafana_secret_id options in config.env must be entered correctly (grafana_secret_id should refer to the name of the secret in AWS Secrets Manager)
- Grafana API Key must have correct permissions (must be Editor or Admin) and that it has not expired. [See this file](https://github.com/k8-proxy/aws-jmeter-test-engine/blob/master/jmeter-icap-poc/instructions/how-to-use-create_dashboards-script.md) for more information on how to create a Grafana API Key.
- If using a custom Grafana URL, make sure the correct port is being used (default port is 3000)
- The machine running this script must have access to the server holding the Grafana instance (i.e. the pod containing the Grafana installation allows the machine running this script to enter).
- The Grafana JSON template should be formatted correctly, for more information refer to the [Grafana Dashboard API](https://grafana.com/docs/grafana/latest/http_api/dashboard/).
