resource "null_resource" "cluster_config" {

  depends_on = [
    azurerm_kubernetes_cluster.default
  ]

  provisioner "local-exec" {

    command     = "az aks get-credentials --resource-group ${local.resource_group} --name ${local.cluster_name} --overwrite-existing"
    interpreter = var.cluster_interpreter
  }
}

resource "null_resource" "helm" {

  depends_on = [
    null_resource.cluster_config
  ]

  provisioner "local-exec" {
    command     = var.helm_permissions
    interpreter = var.cluster_interpreter
  }
}

resource "null_resource" "common" {

  depends_on = [
    azurerm_kubernetes_cluster_node_pool.common
  ]

  provisioner "local-exec" {
    command     = var.common_chart
    interpreter = var.cluster_interpreter
  }
}

resource "null_resource" "chart_repo_update" {

  depends_on = [
    null_resource.common
  ]

  provisioner "local-exec" {
    command     = var.chart_update
    interpreter = var.cluster_interpreter
  }
}

resource "null_resource" "loki" {

  depends_on = [
    null_resource.chart_repo_update
  ]

  provisioner "local-exec" {
    command     = var.loki_chart
    interpreter = var.cluster_interpreter
  }
}

resource "null_resource" "prometheus" {

  depends_on = [
    null_resource.loki
  ]

  provisioner "local-exec" {
    command     = var.prometheus_chart
    interpreter = var.cluster_interpreter
  }
}