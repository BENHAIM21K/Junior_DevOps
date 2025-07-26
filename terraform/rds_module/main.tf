data "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = var.db_secret_name
}

locals {
  secret = jsondecode(data.aws_secretsmanager_secret_version.db_credentials.secret_string)
}

resource "aws_db_subnet_group" "default" {
  name       = "${var.db_name}-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "${var.db_name}-subnet-group"
  }
}

resource "aws_db_instance" "this" {
  identifier              = "${var.db_name}-db"
  engine                  = var.engine
  instance_class          = var.env == "prod" ? "db.t3.small" : "db.t3.micro"
  allocated_storage       = 20
  db_name                 = var.db_name
  username                = local.secret.username
  password                = local.secret.password
  skip_final_snapshot     = true
  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids  = []
  publicly_accessible     = false
  multi_az                = false
}
