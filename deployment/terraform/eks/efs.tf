resource "aws_efs_file_system" "example" {


  creation_token = "${local.cluster_name}"

  tags = {
    Name = "${local.cluster_name}-disk"
  }
}

resource "aws_efs_mount_target" "example" {

  depends_on = [
    module.vpc.private_subnets
  ]
  count           = 2
  file_system_id  = aws_efs_file_system.example.id
  subnet_id       = module.vpc.private_subnets[count.index]
  security_groups = [module.eks.worker_security_group_id]
}