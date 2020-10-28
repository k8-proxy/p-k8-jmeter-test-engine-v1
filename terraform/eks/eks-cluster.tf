module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = local.cluster_name
  cluster_version = "1.17"
  subnets         = module.vpc.private_subnets

  tags = {
    Environment = "glasswall-test"
  }

  vpc_id = module.vpc.vpc_id

  worker_groups = [
    {
      name                          = "worker-group-1"
      instance_type                 = "m4.2xlarge"
      additional_userdata           = "echo foo bar"
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_one.id]
      asg_desired_capacity          = 2
      asg_max_size                  = 1000
      kubelet_extra_args            = "--node-labels=purpose=jmeter --register-with-taints=sku=jmeter:NoSchedule"
    },
    {
      name                          = "worker-group-2"
      instance_type                 = "m4.xlarge"
      additional_userdata           = "echo foo bar"
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_two.id]
      asg_desired_capacity          = 1
      asg_max_size                  = 50
      kubelet_extra_args            = "--node-labels=key=monitoring --register-with-taints=key=monitoring:NoSchedule"
    },
    {
      name                          = "worker-group-3"
      instance_type                 = "m4.xlarge"
      additional_userdata           = "echo foo bar"
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_two.id]
      asg_desired_capacity          = 1
      asg_max_size                  = 50
    }
  ]
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}
