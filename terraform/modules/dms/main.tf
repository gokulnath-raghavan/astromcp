resource "aws_dms_replication_instance" "main" {
  allocated_storage            = var.replication_instance_storage
  apply_immediately           = true
  auto_minor_version_upgrade  = true
  availability_zone           = var.availability_zone
  engine_version              = var.engine_version
  kms_key_arn                 = aws_kms_key.dms.arn
  multi_az                    = var.environment == "prod"
  preferred_maintenance_window = "sun:10:30-sun:14:30"
  publicly_accessible         = false
  replication_instance_class  = var.replication_instance_class
  replication_instance_id     = "${var.environment}-dms-replication-instance"
  replication_subnet_group_id = aws_dms_replication_subnet_group.main.id
  vpc_security_group_ids      = [aws_security_group.dms.id]

  tags = {
    Environment = var.environment
    Name        = "${var.environment}-dms-replication-instance"
  }
}

resource "aws_dms_replication_subnet_group" "main" {
  replication_subnet_group_id          = "${var.environment}-dms-subnet-group"
  replication_subnet_group_description = "DMS subnet group for ${var.environment}"
  subnet_ids                          = var.subnet_ids

  tags = {
    Environment = var.environment
    Name        = "${var.environment}-dms-subnet-group"
  }
}

resource "aws_dms_endpoint" "source" {
  endpoint_id   = "${var.environment}-dms-source-endpoint"
  endpoint_type = "source"
  engine_name   = var.source_endpoint.engine_name
  server_name   = var.source_endpoint.server_name
  port          = var.source_endpoint.port
  username      = var.source_endpoint.username
  password      = var.source_endpoint.password
  database_name = var.source_endpoint.database_name

  tags = {
    Environment = var.environment
    Name        = "${var.environment}-dms-source-endpoint"
  }
}

resource "aws_dms_endpoint" "target" {
  endpoint_id   = "${var.environment}-dms-target-endpoint"
  endpoint_type = "target"
  engine_name   = var.target_endpoint.engine_name
  server_name   = var.target_endpoint.server_name
  port          = var.target_endpoint.port
  username      = var.target_endpoint.username
  password      = var.target_endpoint.password
  database_name = var.target_endpoint.database_name

  tags = {
    Environment = var.environment
    Name        = "${var.environment}-dms-target-endpoint"
  }
}

resource "aws_dms_replication_task" "main" {
  for_each = var.replication_tasks

  migration_type            = each.value.migration_type
  replication_instance_arn = aws_dms_replication_instance.main.replication_instance_arn
  replication_task_id      = "${var.environment}-${each.key}"
  source_endpoint_arn      = aws_dms_endpoint.source.endpoint_arn
  target_endpoint_arn      = aws_dms_endpoint.target.endpoint_arn
  table_mappings           = each.value.table_mappings

  tags = {
    Environment = var.environment
    Name        = "${var.environment}-${each.key}"
  }
}

resource "aws_security_group" "dms" {
  name        = "${var.environment}-dms-sg"
  description = "Security group for DMS replication instance"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
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
    Name        = "${var.environment}-dms-sg"
  }
}

resource "aws_kms_key" "dms" {
  description             = "KMS key for DMS encryption"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = {
    Environment = var.environment
    Name        = "${var.environment}-dms-kms-key"
  }
}

resource "aws_kms_alias" "dms" {
  name          = "alias/${var.environment}-dms-kms-key"
  target_key_id = aws_kms_key.dms.key_id
} 