resource "null_resource" "cluster_config" {

  depends_on = [
    module.eks.workers_asg_arns
  ]

  provisioner "local-exec" {
    command     = var.cluster_config
    interpreter = var.cluster_interpreter
  }
}


resource "null_resource" "storage" {

  depends_on = [
    module.eks.workers_asg_arns
  ]

  provisioner "local-exec" {
    command     = var.persistent_storage
    interpreter = var.cluster_interpreter
  }
}


resource "null_resource" "common_config" {

  depends_on = [
    null_resource.cluster_config
  ]

  provisioner "local-exec" {
    command     = var.common_resources
    interpreter = var.cluster_interpreter
  }
}



resource "null_resource" "common" {

  depends_on = [
    null_resource.common_config
  ]

  provisioner "local-exec" {
    command     = var.common_chart
    interpreter = var.cluster_interpreter
  }
}
