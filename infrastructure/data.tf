data "aws_caller_identity" "current" {}

data "template_file" "ec2-startup" {
  template = file("${path.module}/ec2_startup.sh")

  # vars = {
  #   DOCKER_IMAGE_NAME = docker_registry_image.website.name
  # }
}