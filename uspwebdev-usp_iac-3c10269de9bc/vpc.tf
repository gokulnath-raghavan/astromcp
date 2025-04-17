
resource "aws_eip" "nat" {
  count  = terraform.workspace == "dev" || terraform.workspace == "test" || terraform.workspace == "prod"  ? 1 : 0
  vpc   = true
}


##########################################################################################
# VPC's
##########################################################################################
module "usp_vpc" {
  source = "./modules/vpc"
  count  = terraform.workspace == "dev" || terraform.workspace == "test" || terraform.workspace == "prod"  ? 1 : 0

  name = var.usp_aws_network.lake_vpc_name
  cidr = var.usp_aws_network.lake_aws_vpc_cidr

  azs              = var.usp_aws_network.lake_aws_zones
  private_subnets  = var.usp_aws_network.lake_private_subnets
  public_subnets   = var.usp_aws_network.lake_public_subnets
  database_subnets = var.usp_aws_network.lake_database_subnets

  create_database_subnet_group  = false
  manage_default_network_acl    = true
  default_network_acl_tags      = { Name = "${var.usp_prefix}-${terraform.workspace}-acl" }
  manage_default_route_table    = true
  default_route_table_tags      = { Name = "${var.usp_prefix}-${terraform.workspace}-rt" }
  manage_default_security_group = true
  default_security_group_tags   = { Name = "${var.usp_prefix}-${terraform.workspace}-sg" }
  default_security_group_ingress = var.default_security_group_ingress
  default_security_group_egress = var.default_security_group_egress

  enable_dns_hostnames = true
  enable_dns_support   = true

  external_nat_ip_ids = aws_eip.nat.*.id
  enable_nat_gateway  = true
  single_nat_gateway  = true

  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  create_flow_log_cloudwatch_iam_role  = true
  flow_log_max_aggregation_interval    = 60

  tags     = merge(var.common_tags, var.vpc_tags)
  vpc_tags = var.vpc_tags
}

module "usp_vpc_endpoints" {
  source  = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"
  version = "3.14.0"
  count  = terraform.workspace == "dev" || terraform.workspace == "test" || terraform.workspace == "prod"  ? 1 : 0
  vpc_id             = one(module.usp_vpc[*].vpc_id)
  security_group_ids = module.usp_vpc[*].default_security_group_id

  endpoints = {
    s3 = {
      service      = "s3"
      service_type = "Gateway"
      route_table_ids = flatten([
        module.usp_vpc[*].private_route_table_ids,
        module.usp_vpc[*].public_route_table_ids])
      tags = {
        Name = "${var.usp_s3_env}-s3-vpc-endpoint"
      }
    }
  }

  tags = var.common_tags
}
