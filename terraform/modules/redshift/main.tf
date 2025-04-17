resource "aws_redshift_cluster" "main" {
  cluster_identifier  = var.redshift_cluster_identifier
  database_name      = var.redshift_database_name
  master_username    = var.redshift_master_username
  master_password    = var.redshift_master_password
  node_type          = var.redshift_node_type
  number_of_nodes    = var.redshift_number_of_nodes
  cluster_type       = "multi-node"
  
  vpc_security_group_ids = [aws_security_group.redshift.id]
  cluster_subnet_group_name = aws_redshift_subnet_group.main.name
  
  skip_final_snapshot = var.environment != "prod"
  final_snapshot_identifier = "${var.redshift_cluster_identifier}-final-snapshot"
  
  logging {
    enable        = true
    bucket_name   = aws_s3_bucket.logs.bucket
    s3_key_prefix = "redshift-logs"
  }
  
  tags = {
    Environment = var.environment
    Name        = var.redshift_cluster_identifier
  }
}

resource "aws_redshift_subnet_group" "main" {
  name       = "${var.redshift_cluster_identifier}-subnet-group"
  subnet_ids = var.subnet_ids
  
  tags = {
    Environment = var.environment
    Name        = "${var.redshift_cluster_identifier}-subnet-group"
  }
}

resource "aws_security_group" "redshift" {
  name        = "${var.redshift_cluster_identifier}-sg"
  description = "Security group for Redshift cluster"
  vpc_id      = var.vpc_id
  
  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Environment = var.environment
    Name        = "${var.redshift_cluster_identifier}-sg"
  }
}

resource "aws_s3_bucket" "logs" {
  bucket = "${var.redshift_cluster_identifier}-logs"
  
  tags = {
    Environment = var.environment
    Name        = "${var.redshift_cluster_identifier}-logs"
  }
}

resource "aws_s3_bucket_versioning" "logs" {
  bucket = aws_s3_bucket.logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
} 