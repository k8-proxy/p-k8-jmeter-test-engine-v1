# 100k traffic generation

## 0. Prerequisites

An MS  Azure cluster which allows the utilization of node pools with a sufficient number of pods.
The whole number of working pods with X number of concurrent threads per pod is `100 000 / X`
The number of concurrent threads is defined by the following line

```
    <stringProp name="ThreadGroup.num_threads">X</stringProp>
```
in https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/src/controller/docker-jmeter-c-icap/ICAP-POC_s3.jmx

## 1. Setting up the node pools
The details instruction for this step is located at https://github.com/MariuszFerdyn/p-k8-jmeter-test-engine/blob/master/ManualAKSCreation.MD

##2. Setting up the common resources
Create Minio, Influxdb, and Grafana services in the cluster
Follow instructions at https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/kubernetes/common_resources/README.md

### 2.1 Influx JMeter Database
The cluster InfluxDB deployment must have a database called JMeter
To create it enter the bash shell of the influxdb pod
```
    kubectl exec -it <influxdb pod> -- bash
```
Then create the DB with the following commands
```
    # influx
    > database create jmeter
    > exit
    # exit
```

### 2.2 The Grafana dashboard
The Grafana dashboard that reflects data changes in influx JMeter DB is located at https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/src/grafana_dashboards/ICAP-Dashboard-4-grafana.json
Import it to the Grafana cluster deployment

### 2.3 Input files in Minio
Make sure your Minio deployment has input files in the `input` bucket

## 3. Configuring and running the working pods
As mentioned in the Prerequisites section, the number of necessary working pods is determined by the following `100 000 / X` where is the number of concurrent threads in https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/src/controller/docker-jmeter-c-icap/ICAP-POC_s3.jmx

The current settings have been tested with 25 concurrent threads per pod. This means that to generate 100K traffic 4000 pods will be necessary

In https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/src/controller/docker-jmeter-c-icap/jmeter-job-tmpl.yaml change `parallelism` value to 4000. 
In your PowerShell navigate to `...p-k8-jmeter-test-engine/tree/master/src/controller/docker-jmeter-c-icap` folder. Run the following command:
```
    PowerShell -ExecutionPolicy ByPass -File run.ps1 ICAP-POC_s3.jmx files.txt 1
```

