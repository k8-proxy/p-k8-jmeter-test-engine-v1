variable "region" {
  description = "AWS region"
}

variable "bucket" {
  description = "AWS S3 bucket for state"
}

variable "vpc_name" {
  description = "AWS VPC Name"
}

variable "cluster_name" {
  description = "EKS Cluster Name"
}


variable m4_x_spot_price {
  type        = map
  description = "Spot Instance price based on region"
  default = {
    us-west-1 = "0.080"
    eu-west-1 = "0.289"
  }
}

variable m4_2x_spot_price {
  type        = map
  description = "Spot Instance price based on region"
  default = {
    us-west-1 = "0.140"
    eu-west-1 = "0.569"
  }
}

variable cluster_config {
  type    = string
  default = "aws eks --region eu-west-1 update-kubeconfig --name glasswall-test-cluster"
}

variable persistent_storage {
  type    = string
  default = "kubectl apply -k 'github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master'"
}

variable cluster_autoscaler {
  type    = string
  default = "kubectl apply -f cluster-autoscaler-autodiscover.yaml"
}

variable helm_permissions {
  type    = string
  default = "kubectl create serviceaccount --namespace kube-system tiller ;kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller ; sleep 30  ;helm init --service-account tiller --override spec.selector.matchLabels.'name'='tiller',spec.selector.matchLabels.'app'='helm' --output yaml | sed 's@apiVersion: extensions/v1beta1@apiVersion: apps/v1@' | kubectl apply -f - \n"
}

variable common_chart {
  type    = string
  default = "sleep 40 ; helm upgrade --install common --namespace=common  ../../helm-charts/common-resources/ -f ../../helm-charts/common-resources/aws.yaml "
}

variable chart_update {
  type    = string
  default = "sleep 20 ; helm repo add loki https://grafana.github.io/loki/charts ; helm repo add prometheus-community https://prometheus-community.github.io/helm-charts; helm repo update"
}

variable loki_chart {
  type    = string
  default = "helm upgrade --install loki --namespace=common loki/loki-stack"
}

variable promtail_logs {
  type    = string
  default = "helm upgrade --install promtail --namespace=common loki/promtail --set "loki.serviceName=loki""
}

variable prometheus_chart {
  type    = string
  default = "helm upgrade --install  prometheus --namespace=common stable/prometheus"
}

variable cluster_interpreter {
  type    = list(string)
  default = ["/bin/sh", "-c"]
}
