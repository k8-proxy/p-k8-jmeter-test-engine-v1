resource "aws_iam_role_policy_attachment" "persistent_volumes" {
  policy_arn = aws_iam_policy.persistent_volume.arn
  role       = module.eks.worker_iam_role_name
}

resource "aws_iam_policy" "persistent_volume" {
  name_prefix = "eks-worker-persistent_volume-${local.cluster_name}"
  description = "EKS worker node autoscaling policy for cluster ${local.cluster_name}"
  policy      = data.aws_iam_policy_document.persistent_volume.json
  #path        = var.iam_path
}

data "aws_iam_policy_document" "persistent_volume" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:AttachVolume",
      "ec2:CreateSnapshot",
      "ec2:CreateTags",
      "ec2:CreateVolume",
      "ec2:DeleteSnapshot",
      "ec2:DeleteTags",
      "ec2:DeleteVolume",
      "ec2:DescribeInstances",
      "ec2:DescribeSnapshots",
      "ec2:DescribeTags",
      "ec2:DescribeVolumes",
      "ec2:DetachVolume"
    ]

    resources = ["*"]
  }
}