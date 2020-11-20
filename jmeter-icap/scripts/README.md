# Using create_stack_dash.py to Create Load Generators and Corresponding Dashboards


## Table of Contents
  * [Introduction](#introduction)
  * [Prerequisites](#prerequisites)
  * [Using config.env to pass parameters to create_stack_dash.py](#using-configenv-to-pass-parameters-to-create_stack_dashpy)
  * [Options available for the create_stack_dash.py script](#optionsparameters-available-for-the-create_stack_dashpy-script)
  * [How create_stack_dash.py works](#how-create_stack_dashpy-works)
  * [Running the create_stack_dash.py script](#running-the-create_stack_dashpy-script)
  * [Troubleshooting](#troubleshooting)


## Introduction

This script launches a Cloudformation stack that spins up load generators. Then it creates Grafana Dashboards that display various metrics from the load generators.

## Prerequisites

1. Install Python version 3.8 or later (see [Python](https://www.python.org/downloads/))

2. Ensure necessary python packages are installed. This can be done using the following console command:
```
    pip3 install -r requirements.txt
```
Where requirements.txt is located at the following ["link"](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/src/controller/docker-jmeter-c-icap/requirements.txt)

3. When in AWS environment, set AWS authentication for the Cloudformation stack that will be created. This can be done by configuring AWS on the machine running the script using this script. Make sure AWS CLI is installed on the machine and that a user exists with an AWS access key (can be created under IAM, Security Credentials in the AWS console), then run the following commands:

```
aws configure
```

Prompts will appear asking for the following information:

```
AWS Access Key ID:
AWS Secret Access Key:
Default region name:
Default output format [None]:
```

Input the correct values; the last prompt can be left at default by pressing enter and skipping input.

Once configured, the AWS credentials and config files can be found in the AWS folder located in "~/.aws/" on linux systems or "%USERPROFILE%\\.aws" in Windows systems. At the top of the config folder a profile name in brackets should be present (ex: [default], here "default" will be the profile name to use in the config.env file discussed in the next step).

4. Create config.env file by copying the existing [config.env](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/src/controller/docker-jmeter-c-icap/config.env) sample file. Update the values there to correspond to your test setup - [refer to the table of parameters available below](#options-available-for-the-create-stack-dashpy-script)

5. If using AWS Secrets Manager to store the Grafana API Key, a secret name would need to be provided either in the config.env file or via the command line:

```
GRAFANA_SECRET=MyGrafanaSecretName
```

or

```
python create_stack_dash.py -gs MyGrafanaSecretName
```

## Using config.env to pass parameters to create_stack_dash.py

The config.env file is the preferred way to pass parameters to this script, it should be located in the same folder as create_stack_dash. It contains many parameters that translate to options (listed in options section below) when running the script. For a more detailed description of each parameter, [refer to the table of parameters available below](#options-available-for-the-create-stack-dashpy-script). Below is a sample config.env file:

```
AWS_PROFILE_NAME=default
REGION=eu-west-1
TOTAL_USERS=100
USERS_PER_INSTANCE=25
DURATION=300
FILE_LIST=files.csv
MINIO_URL=http://minio.minio.svc.cluster.local:9000
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_INPUT_BUCKET=input
MINIO_OUTPUT_BUCKET=output
INFLUXDB_URL=http://influxdb.influxdb.svc.cluster.local:8086
PREFIX=dash-creation
ICAP_SERVER=gw-icap01.westeurope.azurecontainer.io
GRAFANA_URL=a6f57c69583674ff982787e2cbe95cea-713263438.eu-west-1.elb.amazonaws.com
GRAFANA_KEY=
GRAFANA_FILE=../grafana_dashboards/k8-test-engine-dashboard.json
EXCLUDE_DASHBOARD=0
PRESERVE_STACK=0
```

These parameters have corresponding options that can be used during script execution, they do not have to be set in config.env. Many of the parameters above are also optional, they can be omitted. Any options input manually via the command line will override options within the config.env file. For example, if the config.env file is set to allow dashboard creation:

```
EXCLUDE_DASHBOARD=0
```

But the option to exclude dashboard creation is used:

```
python create_stack_dash.py -x
```
The Dashboard will still not be created (the option -x prevents dashboard creation) despite the content of the config.env file.

## Options/Parameters available for the create_stack_dash.py script

To see the available options for when running the script, use:
```
python create_stack_dash.py -h
```

Below is a table highlighting all the available options. These options correspond to parameters in the config.env file, they share the same names/descriptions and can be used as a reference when creating your own config.env file.

<table>
<tr>
<td width="200"> Option</td> <td> Config.env Parameter </td> <td> Description </td>
</tr>
<tr>
<td> --region </td><td> REGION </td>
<td>
AWS Region to use
</td>
</tr>
<tr>
<td> --total_users, -t </td> <td> TOTAL_USERS </td>
<td>
Total number of users for the test, Default value is 100.
</td>
</tr>
<tr>
<td> --users_per_instance </td> <td> USERS_PER_INSTANCE </td>
<td>
Users per POD. If not specified, the default value of 25 will be used
</td>
</tr>
<tr>
<td> --duration, -d </td><td> DURATION </td>
<td>
Duration of the test, default value: 300 seconds
</td>
</tr>
<tr>
<td> --list </td> <td> FILE_LIST </td>
<td>
The list of the files in the Minio input bucket to be included in the test
</td>
</tr>
<tr>
<td> --minio_url </td> <td> MINIO_URL </td>
<td>
The Minio endpoint URL including the port number. The default value is 'http://minio.minio.svc.cluster.local:9000'
</td>
</tr>
<tr>
<td> --minio_access_key </td> <td> MINIO_ACCESS_KEY </td>
<td>
The Minio access key
</td>
</tr>
<tr>
<td> --minio_secret_key </td> <td> MINIO_SECRET_KEY </td>
<td>
The Minio secret key
</td>
</tr>
<tr>
<td> --minio_input_bucket </td> <td> MINIO_INPUT_BUCKET </td>
<td>
The Minio input bucket. The default value is 'input'
</td>
</tr>
<tr>
<td> --minio_output_bucket </td> <td> MINIO_OUTPUT_BUCKET </td>
<td>
The Minio output bucket. The default value is 'output'
</td>
</tr>
<tr>
<td> --influxdb_url </td><td> INFLUXDB_URL </td>
<td>
IP address or hostname of the Influx Database including the port number. The default value is 'http://influxdb.influxdb.svc.cluster.local:8086'
</td>
</tr>
<tr>
<td>--prefix, -p </td><td> PREFIX </td>
<td>
The prefix used in both the Cloudformation stack name and the name of the Dashboard and measurements created.
</td>
</tr>
<tr>
<td> --icap_server, -e </td><td> ICAP_SERVER </td>
<td>
The ICAP server URL
</td>
</tr>
<tr>
<td> --grafana_url, -g </td><td> GRAFANA_URL </td>
<td>
The URL to the Grafana database's home page (typically this would be the "MachineIP:3000")
</td>
</tr>
<tr>
<td> --grafana_key, -k </td><td> GRAFANA_KEY </td>
<td>
Grafana API Key (<a href="https://github.com/k8-proxy/aws-jmeter-test-engine/blob/master/jmeter-icap-poc/instructions/how-to-use-createDashboards-script.md">see prerequisits in this article on how to generate this</a>).
</td>
</tr>
<tr>
<td> --grafana_file, -f </td><td> GRAFANA_FILE </td>
<td>
Name/path of JSON file that will be used as a template to create Grafana Dashboards.
</td>
</tr>
<tr>
<td> --exclude_dashboard, -x </td><td> EXCLUDE_DASHBOARD (=0 or 1)</td>
<td>
This takes no arguments. If set (ex: create_stack_dash -x), a Grafana dashboard will not be created when the script is run.
</td>
</tr>
<tr>
<td> --preserve_stack, -s </td><td> PRESERVE_STACK (=0 or 1) </td>
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

A successful run should output information on number of number of PODs to be cleated and Grafana dashboard. See the example below:
```
...
INFO:create_stack:Number of pods to be created: 1
job.batch/demo-jmeterjob created
Creating dashboard...
Stack will be deleted after 20.0 minutes
0.0 minutes have elapsed, stack will be deleted in 20.0 minutes
10.0 minutes have elapsed, stack will be deleted in 10.0 minutes
...
```

## Troubleshooting

Below is a list of potential issues end users might face along with some suggested solutions:

### Grafana Dashboard is not being created
- Check that the "exclude_dashboard" option is not enabled
- The grafana_key or grafana_secret_id options in config.env must be entered correctly (grafana_secret_id should refer to the name of the secret in AWS Secrets Manager)
- Grafana API Key must have correct permissions (must be Editor or Admin) and that it has not expired. [See this file](https://github.com/k8-proxy/aws-jmeter-test-engine/blob/master/jmeter-icap-poc/instructions/how-to-use-create_dashboards-script.md) for more information on how to create a Grafana API Key.
- If using a custom Grafana URL, make sure the correct port is being used (default port is 3000)
- The machine running this script must have access to the server holding the Grafana instance (i.e. the EC2 instance containing the Grafana installation has its security group set to allow the machine running this script to enter).
- The Grafana JSON template should be formatted correctly, for more information refer to the [Grafana Dashboard API](https://grafana.com/docs/grafana/latest/http_api/dashboard/).

### EC2 instance containing Grafana installation is not auto-starting
- The machine attempting to start the EC2 instance must have the correct permissions set in the EC2 instance's security group.
- The option grafana_server_tag must be used to start the EC2 instance. It should contain only the value of the tag with a key field containing "Name". See below:

### Stacks are not being automatically deleted
- Ensure the option "preserve_stack" is not enabled
- create_stack_dash.py deletes only the stack that was created in an individual run. If the script is stopped before the delete process takes place (i.e. before the duration period + 15 minutes) for any reason, the stack it created will not be deleted and must be deleted manually.
