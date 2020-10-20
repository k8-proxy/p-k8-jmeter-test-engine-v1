# Health check monitoring of the icap-server

## How JMeter Script works?

Jmeter script is designed to monitor ICAP server metrics.

It basically 
- Run icap client command to fetch ICAP server metrics
- Convert ICAP server metrics to InfluxDB line syntax
- Post InfluxDB line syntax to InfluxDB server as measurements
- Present measurements into Grafana dashboard

## Prerequisites
	docker is installed
	kubernetes is configured already
	InfluxDB Pod is installed
	Grafana Pod is installed

## Usage
Clone/Copy main directory and Test sub-folder to local, the directory look like :

	 Test folder
	      |__FetchICAP_Server_metrics.jmx      
		 |__ICAPServerMonitoring.properties	 
		 |__launch.sh
	   __Dockerfile  
	   __icap_server_monitoring_dashboard.json
	   __IcapMonitoringPod.yaml
	   __Readme.md

### Import Icap server monitoring dashboard to grafana
Open Grafana > Manage Dashboard > import > Select "icap_server_monitoring_dashboard.json" to import

### Setup parameters of Jmeter script
Refer ICAPServerMonitoring.properties to setup parameters accordingly, this file is used to create ConfigMap for Jmeter Pod

### Build Docker image 
Go to main directory and build docker image from dockerfile following command:
```bash
[root@sonha]# docker build --tag icapservermonitoring:1.0 .

```
### Create ConfigMap
run following command to create configmap, it will point all Jmeter parameters to config map and we can easy to change/modify
```bash
[root@sonha]# kubectl create configmap icap-configmap --from-file=ICAPServerMonitoring.properties=./Test/ICAPServerMonitoring.properties

```
### Create Jmeter Pod
Create a pod to run Jmeter script to monitor ICAP server metrics, configMap is used as Jmeter customize properties file
```bash
[root@sonha]# kubectl apply -f IcapMonitoringPod.yaml

```
### Grafana Dashboard monitoring 
Make sure Jmeter POD is created and running, go to grafana, select dashboard and view the ICAP server metrics
  
## License
MIT License
See: LICENSE
