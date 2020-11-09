*** Run Proxy site test ***
- In order to run proxy site test clone the repo - https://github.com/k8-proxy/p-k8-jmeter-test-engine.git
- Navigate to /src/k8-proxy-test
- run below powershell command to deploy pod as job.
- the current setting in jmeter-job-tmpl.yaml is to run 10 pod on job submission. you can modify 

```
parallelism: 10  # increase the number here to get more pods
```
Run this command to deploy job
```
PowerShell -ExecutionPolicy ByPass -File run.ps1  1
```
Run this command to remove job from cluster

```
PowerShell -ExecutionPolicy ByPass -File stop.ps1 
```
The current setup in image is for 500 user per pod. 

In order to monitor the result locally do portforwarding for grafana pod using 

``` 
 kubectl port-forward -n grafana service/grafana-service 3000
 ```
 Navigate to Dashboard/Manage and Select Proxy Test Dashboard if the dashboard is not exits you can import from grafana_dashboards folder

 You need to update math in Number of User / Errors Panel and Active User Panel by clicking on Title/Edit by number of pods you running to get accurate result.

The current Test using Reponse Assertion on Response Header and Response message to validate test.

### Important note about docker image ###
There are two seperate docker image for proxy site test due to diffrent url for influx DB in cluster.

Docker Images List which you can change in jmeter-job-tmpl.yaml depend on Cluster you want to run test on.

Image for Azure - glasswallsolutions/cloud-qa:proxy1.12
Image for EKS - glasswallsolutions/cloud-qa:proxy_EKS_1.8

Influx URL for backend listner in JMX (The above Images have those details already in them so no need to change it)

AKS (Azure) - http://influxdb.influxdb.svc.cluster.local:8086/write?db=proxysite

EKS (AWS) - http://influxdb-service.common:8086/write?db=proxysite


## Docker Image Setup ##

The docker image we are using here is Harden centos 7 Base image.
Installed Dependancy list

 - wget
 - java-1.8.0-openjdk
 - jmeter binary version 5.2.1
 - Url list file as csv
 - jmx script (configured to use url from csv to run test)

 ## Enable Kubernetes Dashboard

In order to access Kubernetes dashboard from local host use below command to do port-forwarding.
```
kubectl port-forward service/kubernetes-dashboard -n kube-system 443
```
Navigate to Browser and open https://localhost/

Follow below steps to get Tocken to access the dashboard

 ```
 kubectl delete clusterrolebinding kubernetes-dashboard
 ```

```
kubectl create clusterrolebinding kubernetes-dashboard --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard --user=clusterUser
``` 
Run below comand and copy Tocken for Relevant cluster
```
kubectl config view --raw
```
