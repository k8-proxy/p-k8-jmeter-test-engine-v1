resource "random_pet" "prefix" {}

provider "azurerm" {
  version = "~> 2.0"
  features {}
}

locals {
  cluster_name   = var.cluster_name
  resource_group = var.resource_group
}

#resource "azurerm_resource_group" "default" {
#  name     = "${random_pet.prefix.id}-rg"
#  location = "West US 2"
#
#  tags = {
#    environment = "Demo"
#  }
#}


resource "azurerm_kubernetes_cluster" "default" {
  name                = local.cluster_name
  location            = "West Europe"
  resource_group_name = local.resource_group
  dns_prefix          = "${random_pet.prefix.id}-k8s"

  default_node_pool {
    name                = "default"
    node_count          = 2
    vm_size             = "Standard_D2_v2"
    os_disk_size_gb     = 30
    enable_auto_scaling = "true"
    type                = "VirtualMachineScaleSets"
    min_count           = 1
    max_count           = 20
  }

  service_principal {
    client_id     = var.appId
    client_secret = var.password
  }

  role_based_access_control {
    enabled = true
  }

  addon_profile {
    kube_dashboard {
      enabled = true
    }
  }

  tags = {
    environment = "Demo"
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "common" {
  name                  = "common"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.default.id
  vm_size               = "Standard_D2_v2"
  node_count            = 2
  enable_auto_scaling   = "true"
  min_count             = 1
  max_count             = 20
  tags = {
    Environment = "Demo"
  }
  node_taints = [
    "key=monitoring:NoSchedule"
  ]
}

resource "azurerm_kubernetes_cluster_node_pool" "jmeter" {
  name                  = "jmeter"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.default.id
  vm_size               = "Standard_D2_v2"
  node_count            = 2
  enable_auto_scaling   = "true"
  min_count             = 1
  max_count             = 100
  tags = {
    Environment = "Demo"
  }
  node_taints = [
    "sku=jmeter:NoSchedule"
  ]
}
