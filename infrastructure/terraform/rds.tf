# RDS Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.app_name}-${var.environment}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name        = "${var.app_name}-${var.environment}-db-subnet-group"
    Environment = var.environment
  }
}

# RDS Security Group
resource "aws_security_group" "rds" {
  name        = "${var.app_name}-${var.environment}-rds-sg"
  description = "Security group for RDS"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.app_name}-${var.environment}-rds-sg"
    Environment = var.environment
  }
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier             = "${var.app_name}-${var.environment}-db"
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = var.database_instance_class
  allocated_storage      = 20
  max_allocated_storage  = 100
  storage_type           = "gp3"
  db_name                = "aws_automation"
  username               = "admin"
  password               = random_password.db_password.result
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  skip_final_snapshot    = var.environment != "prod"
  deletion_protection     = var.environment == "prod"

  tags = {
    Name        = "${var.app_name}-${var.environment}-db"
    Environment = var.environment
  }
}

# Random password for RDS
resource "random_password" "db_password" {
  length  = 32
  special = true
}
