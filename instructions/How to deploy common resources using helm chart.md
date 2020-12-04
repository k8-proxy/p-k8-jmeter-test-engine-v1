# Helm Charts 

## Overview

* [common-resources](https://github.com/k8-proxy/p-k8-jmeter-test-engine/tree/helm-charts/helm-charts/common-resources/)
* [jmeter-testdata] - WIP

## Helm Installation

Refer to this [helm-v2](https://v2.helm.sh/docs/using_helm/#installing-helm)  for installation.


## Helm Permissions

```shell
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'      
helm init --service-account tiller --upgrade
```

## Common Chart Installation

Run below command to install all resources defined in `common-resource` helm chart

```shell
helm install --name common ./common-resources/ -f ./common-resources/aws.yaml  --namespace common
```

## Common Chart Deletion

```shell
helm delete --purge common
```

## Jmeter Chart installation

Run below command to install all resources defined in `jmeter-test` helm chart. Specify the `replicaCount` value to start multiple pods in parallel.

```shell
helm install --name jmeter ./jmeter-test/ --set replicaCount=5
```

## Jmeter Chart Deletion

```shell
helm delete --purge jmeter
```
