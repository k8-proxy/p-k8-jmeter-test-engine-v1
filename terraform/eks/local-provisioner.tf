resource "null_resource" "cluster_config" {

  depends_on = [
    module.eks.workers_asg_arns
  ]

  provisioner "local-exec" {
    command     = "aws eks --region ${var.region} update-kubeconfig --name ${local.cluster_name}"
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

resource "null_resource" "autoscaler_config" {
  depends_on = [
    null_resource.cluster_config
  ]

  provisioner "local-exec" {
    command     = "sed -i -e 's/CLUSTER_NAME/${local.cluster_name}/g' cluster-autoscaler-autodiscover.yaml"
    interpreter = var.cluster_interpreter
  }
}


resource "null_resource" "autoscaler" {

  depends_on = [
    null_resource.autoscaler_config
  ]

  provisioner "local-exec" {
    command     = var.cluster_autoscaler
    interpreter = var.cluster_interpreter
  }
}


resource "null_resource" "storage" {

  depends_on = [
    null_resource.autoscaler
  ]

  provisioner "local-exec" {
    command     = var.persistent_storage
    interpreter = var.cluster_interpreter
  }
}


resource "null_resource" "update_fs_id" {

  depends_on = [
    aws_efs_file_system.example,
    aws_efs_mount_target.example
  ]
  provisioner "local-exec" {
    command     = "sed -i -e 's/EFS-ID/${aws_efs_file_system.example.id}/g' ../../helm-charts/common-resources/aws.yaml"
    interpreter = var.cluster_interpreter
  }
}

resource "null_resource" "common" {

  depends_on = [
    null_resource.helm
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

resource "null_resource" "promtail" {

  depends_on = [
    null_resource.loki
  ]

  provisioner "local-exec" {
    command     = var.promtail_logs
    interpreter = var.cluster_interpreter
  }
}

