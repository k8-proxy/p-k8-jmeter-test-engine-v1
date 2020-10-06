# Deploy applications to K8s cluster

## Setup connection to k8s cluster in Github repo

1. Create a service account with cluster-admin clusterrole which will be used in Github Actions

    kubectl create serviceaccount -n default cd-pipeline
    kubectl create clusterrolebinding cd-pipeline-admin-binding --clusterrole=cluster-admin --serviceaccount=default:cd-pipeline

2. Create below secrets in github repo.

* K8S_URL - Get kubernetes API URL using `kubectl config view --minify -o jsonpath={.clusters[0].cluster.server}`
* K8S_SECRET - Get service account's secret in json format using `kubectl get secret cd-pipeline-token-bjmml -n default -o json`


## Grafana
Set below secrets in Github project before running Github workflow to deploy Grafana

1. GF_USERNAME
2. GF_PASSWORD

Connect to Grafana on http://localhost:3000 using below commands

    kubectl port-forward -n grafana service/grafana-service 3000


## ELK
Connect to Elastic and Kibana using below commands

### Check the credentials
Username: elastic Password: see command below

    kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'

Open Kibana on https://localhost:5601

    kubectl port-forward -n elk service/quickstart-kb-http 5601

## Minio
Set below secrets in Github project before running Github workflow to deploy Minio

1. MINIO_ACCESS_KEY
2. MINIO_SECRET_KEY

Connect to Minio on http://localhost:9000 by running below commands

    kubectl port-forward -n minio service/minio 9000


## InfluxDB

Connect to InfluxDB on http://localhost:8086 by running below commands

    kubectl port-forward -n inlfuxdb service/influxdb 8086
### Create DB
> create database jmeter;

## Prometheus

Connect to Prometheus server on http://localhost:9090 URL by running these commands:
    
    kubectl --namespace prometheus port-forward service/prometheus-server 9090:80
