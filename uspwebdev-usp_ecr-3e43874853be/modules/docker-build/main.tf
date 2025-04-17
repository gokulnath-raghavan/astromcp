# Checks if MD5 of build folder has changed
data "external" "build_folder" {
  program = ["bash", "${path.module}/bin/image_md5.sh", var.dockerfile_folder]
}

# Builds test-service and pushes it into aws_ecr_repository
resource "null_resource" "build_and_push" {
  triggers = {
    build_folder_content_md5 = data.external.build_folder.result.md5
  }

  # See build.sh for more details
  provisioner "local-exec" {
    command = "${path.module}/bin/build_image.sh ${var.dockerfile_folder} ${var.ecr_repository_url}:${var.docker_image_tag} ${var.aws_region}"
    interpreter = ["bash", "-c"]
  }
}
