#!/bin/bash

sudo pkill kubectl -9

if ! type "microk8s.kubectl" > /dev/null; then

        if [[ $(kubectl get pods -A | grep minio | grep Running) ]]; then
                kubectl port-forward -n common service/minio-service 9000:80 &
        else
                echo "minio-service not Running"
        fi

        if [[ $(kubectl get pods -A | grep grafana | grep Running) ]]; then
                kubectl port-forward -n common service/grafana-service 3000:80 &
        else
                echo "grafana-service not Running"
        fi

else
        if [[ $(sudo microk8s.kubectl get pods -A | grep minio | grep Running) ]]; then
                microk8s.kubectl port-forward -n common service/minio-service 9000:80 &
        else
                echo "minio-service not Running"
        fi

        if [[ $(sudo microk8s.kubectl get pods -A | grep grafana | grep Running) ]]; then
                microk8s.kubectl port-forward -n common service/grafana-service 3000:80 &
        else
                echo "grafana-service not Running"
        fi
fi
