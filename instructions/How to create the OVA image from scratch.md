# How to create the OVA image from scratch

## Introduction 

The process described in the document utilizes VMware Workstation as a Hypervisor. <br/>
The process (with some minor adjustments) must be applied to be run on other [Hypervisors](https://en.wikipedia.org/wiki/Hypervisor) as well.

## Provisioning a Virtual Machine

- Download ISO for the latest version of [Ubuntu](https://ubuntu.com/download/desktop) 
- In a VMware workstation create a VM with at least 6 GB of RAM and 40 GB of the hard drive. Follow VMware [instructions](https://kb.vmware.com/s/article/1018415)

## Creating a local Kubernetes node

The kubernetes environemet utilize [microk8s](https://microk8s.io/). <br/>
Follow instructions for Linux to install it in your newly created VM <br/>
Make sure you have access to the internet. 

```
    ping yahoo.com
```
In case the internet is not accessible configure the network by following the [instucsions](https://www.howtoforge.com/linux-basics-set-a-static-ip-on-ubuntu)

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

## Upload test files to the Minio server

## Add Data sources in Grafana

## Create the OVA

- Shut down the VM
- Follow the instruction for [Exporting a VM to OVF/OVA format](https://docs.vmware.com/en/VMware-Fusion/11/com.vmware.fusion.using.doc/GUID-16E390B1-829D-4289-8442-270A474C106A.html)