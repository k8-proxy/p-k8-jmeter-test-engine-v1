# How to create the OVA image from scratch

## Introduction 

The process described in the document utilizes VMware Workstation as a Hypervisor. <br/>
With some minor adjustments, the process may be applied to other [Hypervisors](https://en.wikipedia.org/wiki/Hypervisor) as well.

## Provisioning a Virtual Machine

- Download ISO for the latest version of [Ubuntu](https://ubuntu.com/download/desktop) 
- In a VMware workstation create a VM with at least 6 GB of RAM and 40 GB of the hard drive. Follow VMware [instructions](https://kb.vmware.com/s/article/1018415)

When creating a VM choose advanced settings and choose `Workstation 10` hardware compatibility mode. <br/>
This will allow the VM to run on most modern VMware hypervisors.

## Creating a local Kubernetes node

Make sure you have access to the internet. 

```
    ping yahoo.com
```
In case the internet is not accessible configure the network by following the [instucsions](https://www.howtoforge.com/linux-basics-set-a-static-ip-on-ubuntu)<br/>
<br/>
As a kubernetes environemet utilize [microk8s](https://microk8s.io/). <br/>
Follow instructions for [Linux](https://microk8s.io/) to install it in your newly created VM <br/>

## kubectl alias

microk8s has its custom implementation of kubectl which may be invoked with 

```
    sudo microk8s kubectl
```
To make it in as a regular `kubectl` crete the following alias 
```
    alias kubectl="sudo microk8s kubectl"
```
## Install helm

To install helm run the following commands in the terminal:
```
    curl -LO https://git.io/get_helm.sh
    chmod 700 get_helm.sh
    ./get_helm.sh
    helm init
    helm repo add stable https://charts.helm.sh/stable
    helm repo update
```

## Clone this repo

```
    cd ~
    git clone https://github.com/k8-proxy/p-k8-jmeter-test-engine.git
```

## Install common resources

```
    cd ~/p-k8-jmeter-test-engine/deployment/helm-charts/
    helm upgrade --install common ./common-resources/ -f ./common-resources/local.yaml  --namespace common
```

## Install Loki and Promtail

```
    helm repo add loki https://grafana.github.io/loki/charts
    helm repo update
    helm upgrade --install loki --namespace=common loki/loki-stack
    helm upgrade --install promtail --namespace=common loki/promtail --set "loki.serviceName=loki"   
```
# Angular UI Component Installation and Deployment

## Prerequisites

Install Node.js

```bash
sudo apt install nodejs -y
sudo apt install npm -y
sudo npm install -g @angular/cli
sudo npm install -g http-server
```
Install python

```bash
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```
For back end, install Flask and dependencies. A requirements file is already set up and can be used to get the necessary packages. Navigate to folder and install:

```
cd /p-k8-jmeter-test-engine/jmeter-icap/scripts
sudo pip3 install -r requirements.txt
```

## Setting up UI Project from Repository

To install the Angular project and all dependencies, navigate to the folder containing the project files in the repository and use npm like so:
```
cd /p-k8-jmeter-test-engine/UI/master-script-form
sudo npm install
```
This will automatically download all dependencies and setup files/folders required to test/develop/deploy this angular project. It could take a couple of minutes to install.

## Deploying Angular Project 

Deploying UI for Local run, in the terminal, run:
```
cd /p-k8-jmeter-test-engine/UI/master-script-form
ng serve
```
once is successfully run you will get url for Test UI 

Now the UI should be accessible via http://localhost:4200/ 

## Deploying Angular Project to Web Server

The project must first be built in order to be deployed. In the project directory, in the terminal, run:
```
cd /p-k8-jmeter-test-engine/UI/master-script-form
sudo ng build --prod
```

This will generate a dist folder that contains the files that need to be copied into the apache server.

```
sudo cp -a /p-k8-jmeter-test-engine/UI/master-script-form/dist/master-script-form/. /var/www/html/
```

Now the UI should be accessible via the virtual machine's IP (i.e. http://virtual-macine-ip)

## Setting Up Backend Server as a Service

To setup the backend service, navigate to the folder containing the project files in the repository and copy the flask.service file to the system folder, and provide "exec.sh" with the correct permissions as shown below:
```
cd /p-k8-jmeter-test-engine/jmeter-icap/scripts
sudo chmod +x exec.sh
sudo cp flask.service /etc/systemd/system/
```

Flask.service's contents point to the directory where the project's python server scripts exist and to exec.sh, which runs those scripts. Please ensure that *WorkingDirectory* and *ExecStart* paths match the project repository path (they should by default):

```
# /etc/systemd/system/flask.service
[Unit]
Description=WSGI App for ICAP Testing UI Front End
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/usr/glasswall/home/p-k8-jmeter-test-engine/jmeter-icap/scripts
ExecStart=/usr/glasswall/home/p-k8-jmeter-test-engine/scripts/exec.sh
Restart=always

[Install]
WantedBy=multi-user.target
```


Once flask.service is put into "/etc/systemd/system/" and contains the correct directory information, it will have to be enabled then started.
To do this, run the following:

```
sudo systemctl enable flask
sudo systemctl start flask
```

Check if the service is running correctly using:

```
sudo systemctl status flask
```

The service should now be started and running in the background. To view this service's logs, use the following:

```
sudo journalctl -u flask
```


## Upload test files to the Minio server

At this moment you must have minio service running in your microk8s environemnt<br/>
Make it accessible in the browser with the following command
```
    kubectl port-forward -n common service/minio-service --address 0.0.0.0 9000:80
```
The command above will allow to access the local minio service with the VM IP address from outside the VM as well. <br/>
The URL will be Minio http://vm-ip-address:9000.<br/>
Now you can utilize [s3-to-minio](https://github.com/k8-proxy/p-k8-jmeter-test-engine/tree/master/jmeter-icap/scripts/s3-to-minio) script to upload the test date from AWS S3 to the minio server

## Grafana settings

Run the following command in the terminal
```
    kubectl port-forward -n common service/grafana-service 3000:80
```
Access Grafana in the local browser with URL http://localhost:3000 <br/>
Add the following Grafana data sources: <br/> 

a) Name: icapserver <br/> 
   Querly language: InfluxQL <br/> 
   URL: http://influxdb-service.common <br/> 
   Database: icapserver <br/> 

b) Name: InfluxDB <br/> 
   Querly language: InfluxQL <br/> 
   URL: http://influxdb-service.common <br/> 
   Database: jmeter <br/> 

c) Name: Loki <br/> 
   URL: http://loki.common:3100 <br/> 
 
Generate and safe a Grafana API key to be utilized on the next step.

## Adjust the config.env
Edit settings for running the master traffic generation script
```
    cd ~/p-k8-jmeter-test-engine/jmeter-icap/scripts/
    nano config.env
```
config.env content should look similar to the following:
```
WS_PROFILE_NAME=default
REGION=eu-west-1
TOTAL_USERS=25
USERS_PER_INSTANCE=25
DURATION=300
TEST_DATA_FILE=../scripts/ICAP-Direct-File-Processing/gov_uk_files.csv
MINIO_URL=http://minio-service.common:80
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin@123
MINIO_INPUT_BUCKET=icap-performance-test-data-bucket
MINIO_OUTPUT_BUCKET=output
INFLUXDB_URL=http://influxdb-service.common:80
PREFIX=test
ICAP_SERVER_URL=eu.icap.glasswall-icap.com
GRAFANA_URL=localhost:3000
GRAFANA_API_KEY=eyJrIjoiZE9FWGt5MDl6Qld4VlhzcHd3TzVyWGh3MUJZZzkyNmEiLCJuIjoiSk1ldGVyIHRlc3QiLCJpZCI6MX0=
GRAFANA_FILE=../grafana_dashboards/k8-test-engine-dashboard.json
EXCLUDE_DASHBOARD=0
PRESERVE_STACK=0
ICAP_SERVER_PORT=1344
ENABLE_TLS=0
TLS_VERIFICATION_METHOD=no-verify
JMX_FILE_PATH=ICAP-Direct-File-Processing/ICAP_Direct_FileProcessing_k8_v3.jmx
```

## Create the OVA

- Shut down the VM
- Follow the instruction for [Exporting a VM to OVF/OVA format](https://docs.vmware.com/en/VMware-Fusion/11/com.vmware.fusion.using.doc/GUID-16E390B1-829D-4289-8442-270A474C106A.html)