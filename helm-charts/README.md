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

## Chart Installation

Run below command to install all resources defined in `common-resource` helm chart

```shell
helm install --name common ./common-resources/ -f ./common-resources/aws.yaml  --namespace common
```

## Chart Deletion

```shell
helm delete --purge common
```