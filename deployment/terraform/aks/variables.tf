variable "appId" {
  description = "Azure Kubernetes Service Cluster service principal"
}

variable "password" {
  description = "Azure Kubernetes Service Cluster password"
}

variable "resource_group" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable helm_permissions {
  type    = string
  default = "kubectl create serviceaccount --namespace kube-system tiller ;kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller ; sleep 30  ;helm init --service-account tiller --override spec.selector.matchLabels.'name'='tiller',spec.selector.matchLabels.'app'='helm' --output yaml | sed 's@apiVersion: extensions/v1beta1@apiVersion: apps/v1@' | kubectl apply -f - \n"
}

variable common_chart {
  type    = string
  default = "sleep 40 ; helm upgrade --install common --namespace=common  ../../helm-charts/common-resources/ -f ../../helm-charts/common-resources/azure.yaml "
}

variable chart_update {
  type    = string
  default = "sleep 20 ; helm repo add loki https://grafana.github.io/loki/charts ; helm repo add prometheus-community https://prometheus-community.github.io/helm-charts; helm repo update"
}

variable loki_chart {
  type    = string
  default = "helm upgrade --install loki --namespace=common loki/loki-stack"
}

variable prometheus_chart {
  type    = string
  default = "helm upgrade --install  prometheus --namespace=common stable/prometheus"
}

variable cluster_interpreter {
  type    = list(string)
  default = ["/bin/sh", "-c"]
}