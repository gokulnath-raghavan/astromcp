# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "edw-redshift-cluster-dev"
resource "aws_redshift_cluster" "redshift-cluster-dev" {
  allow_version_upgrade                = true
  apply_immediately                    = null
  automated_snapshot_retention_period  = 1
  availability_zone                    = "us-east-1b"
  availability_zone_relocation_enabled = false
  cluster_identifier                   = "edw-redshift-cluster-dev"
  cluster_parameter_group_name         = "default.redshift-1.0"
  cluster_public_key                   = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCbuFjTQTWlPKkIaMluXg7hr//DypSEJZWAtv7sbjz87RRwI21RAwVWqMn44tbRdpGIY9GREb/4tSo4EPNwvDiKV3LYrBoKsVJ3mD6H4DEDAhZYe/ePL02LXRkc4ZJNIHY7x7BkfI7sZ4u8Pc6SEzTLQOire3VH4tvrj2GsWzpR/bGS5jm3nriSA2U4PPZzC64CPFC0O2rHToRTmezsDoMXVkJWmqk2Sc+QqDF+0tD6ly/A3epx8BFdjqmqtgn75RtT12GGtlBpR8DrlEOHW/1JexcRM0W1lSedhmEDLKjk5hziz7n2VOe9QXUQp5OFOKr0BNUS2PdIzVFDhPwH0QLh Amazon-Redshift\n"
  cluster_revision_number              = jsonencode(109616)
  cluster_subnet_group_name            = "edw-redshift-cluster-dev-private-subnet-group"
  cluster_type                         = "single-node"
  cluster_version                      = jsonencode(1)
  database_name                        = null
  default_iam_role_arn                 = null
  elastic_ip                           = null
  encrypted                            = false
  endpoint                             = "edw-redshift-cluster-dev.cpp2phqw0iay.us-east-1.redshift.amazonaws.com:5439"
  enhanced_vpc_routing                 = false
  final_snapshot_identifier            = null
  iam_roles                            = ["arn:aws:iam::574445142477:role/dms-access-for-endpoint", "arn:aws:iam::574445142477:role/dms-redshift-s3-role"]
  kms_key_id                           = null
  maintenance_track_name               = "current"
  manage_master_password               = null
  manual_snapshot_retention_period     = 7
  master_password                      = null # sensitive
  master_password_secret_kms_key_id    = null
  master_password_wo                   = null # sensitive
  master_password_wo_version           = null
  master_username                      = "admin"
  multi_az                             = false
  node_type                            = "ra3.large"
  number_of_nodes                      = 1
  owner_account                        = null
  port                                 = 5439
  preferred_maintenance_window         = "wed:03:00-wed:03:30"
  publicly_accessible                  = false
  skip_final_snapshot                  = true
  snapshot_arn                         = null
  snapshot_cluster_identifier          = null
  snapshot_identifier                  = null
  tags = {
    Name = "edw-redshift-cluster-dev"
  }
  tags_all = {
    Name = "edw-redshift-cluster-dev"
  }
  vpc_security_group_ids = ["sg-07a4221d1abc22795"]
}
