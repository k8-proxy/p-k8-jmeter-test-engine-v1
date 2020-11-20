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

variable cluster_interpreter {
  type    = list(string)
  default = ["/bin/sh", "-c"]
}