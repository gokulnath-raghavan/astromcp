locals {
  workspace_uuid = replace(var.workspace_uuid, "/[{}]/", "")

  url = "https://api.bitbucket.org/2.0/workspaces/${var.workspace_name}/pipelines-config/identity/oidc"
  client_id_list = [
    "ari:cloud:bitbucket::workspace/${local.workspace_uuid}"
  ]
  thumbprint_list = concat(var.additional_thumbprints, ["a031c46782e6e6c662c2c87c76da9aa62ccabd8e"])
}

data "aws_region" "current" {}

resource "aws_iam_openid_connect_provider" "bitbucket" {
  url = local.url
  client_id_list = local.client_id_list
  thumbprint_list = local.thumbprint_list
  tags = merge(var.common_tags, { Name = "Bitbucket OpenID provider" } )
}

resource "aws_ecr_repository" "bitbucket_runner" {
  name                 = "bitbucket-runner"
  image_tag_mutability = "IMMUTABLE"
}

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = ["${aws_iam_openid_connect_provider.bitbucket.arn}"]
    }
    
    condition {
      test     = "StringEquals"
      variable = "api.bitbucket.org/2.0/workspaces/${var.workspace_name}/pipelines-config/identity/oidc:aud"
      values = local.client_id_list
    }
  }
}

data "aws_iam_policy_document" "ecr_policy_document" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken"
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:GetRepositoryPolicy",
      "ecr:DescribeRepositories",
      "ecr:ListImages",
      "ecr:DescribeImages",
      "ecr:BatchGetImage"
    ]
    resources = [
      "${aws_ecr_repository.bitbucket_runner.arn}"
    ]
  }
}

data "aws_iam_policy_document" "ecr_access_policy_document" {
  statement {
    effect = "Allow"
    actions = [
      "iam:*",
      "ec2:*",
      "sns:*",
      "events:*",
      "logs:*"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role" "ecr_role" {
  name               = "usp-ecr-access-role"
  assume_role_policy = "${data.aws_iam_policy_document.assume.json}"
}

resource "aws_iam_policy" "ecr_policy" {
  name   = "usp-ecr-policy-prod"
  policy = "${data.aws_iam_policy_document.ecr_policy_document.json}"
}

resource "aws_iam_policy" "ecr_access_policy" {
  name   = "usp-ecr-access-policy"
  policy = "${data.aws_iam_policy_document.ecr_access_policy_document.json}"
}

resource "aws_iam_role_policy_attachment" "ecr_policy_attachment_1" {
  role = "${aws_iam_role.ecr_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "ecr_policy_attachment_2" {
  role = "${aws_iam_role.ecr_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonAthenaFullAccess"
}

resource "aws_iam_role_policy_attachment" "ecr_policy_attachment_3" {
  role = "${aws_iam_role.ecr_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
}

resource "aws_iam_role_policy_attachment" "ecr_policy_attachment_4" {
  role = "${aws_iam_role.ecr_role.name}"
  policy_arn = "${aws_iam_policy.ecr_policy.arn}"
}

resource "aws_iam_role_policy_attachment" "ecr_policy_attachment_5" {
  role = "${aws_iam_role.ecr_role.name}"
  policy_arn = "${aws_iam_policy.ecr_access_policy.arn}"
}

resource "aws_iam_role_policy_attachment" "ecr_policy_attachment_6" {
  role = "${aws_iam_role.ecr_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}

module "ecr_docker_build" {
  source = "./modules/docker-build"

  dockerfile_folder = "./image"
  docker_image_tag = "latest"
  aws_region = "${data.aws_region.current.name}"
  ecr_repository_url = "${aws_ecr_repository.bitbucket_runner.repository_url}"
  depends_on = [aws_iam_role_policy_attachment.ecr_policy_attachment_5]
}
