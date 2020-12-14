#!/bin/bash

sudo pkill kubectl -9

if ! type "microk8s.kubectl" > /dev/null; then

        if [[ $(kubectl -n common get svc | grep minio-service) ]]; then
                echo "minio-service installed"
                kubectl port-forward -n common service/minio-service 9000:80 &
        else
                echo "minio-service not installed"
        fi

        if [[ $(kubectl -n common get svc | grep grafana-service) ]]; then
                echo "grafana-service installed"
                kubectl port-forward -n common service/grafana-service 3000:80 &
        else
                echo "grafana-service not installed"
        fi

else
        if [[ $(sudo microk8s.kubectl -n common get svc | grep minio-service) ]]; then
                echo "minio-service installed"
                microk8s.kubectl port-forward -n common service/minio-service 9000:80 &
        else
                echo "minio-service not installed"
        fi

        if [[ $(sudo microk8s.kubectl -n common get svc | grep grafana-service) ]]; then
                echo "grafana-service installed"
                microk8s.kubectl port-forward -n common service/grafana-service 3000:80 &
        else
                echo "grafana-service not installed"
        fi
fi
