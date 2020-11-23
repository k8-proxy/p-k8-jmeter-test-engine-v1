resource "null_resource" "cluster_config" {

  depends_on = [
    azurerm_kubernetes_cluster.default
  ]

  provisioner "local-exec" {

    command     = "az aks get-credentials --resource-group ${local.resource_group} --name ${local.cluster_name} --overwrite-existing"
    interpreter = var.cluster_interpreter
  }
}