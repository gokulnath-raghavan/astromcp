output "repository_url" {
  description = "The URL of the ECR repository"
  value       = try(aws_ecr_repository.bitbucket_runner.repository_url, "")
}

output "repository_name" {
  description = "The URL of the ECR repository"
  value       = try(aws_ecr_repository.bitbucket_runner.name, "")
}

output "repository_url_of_image" {
  value       = "${module.ecr_docker_build.ecr_image_url}"
  description = "Full URL to image in ecr with tag"
}

output "oidc_role_arn" {
  value       = "${aws_iam_role.ecr_role.arn}"
  description = "OIDC role to access ECR repository"
}
