variable "db_name" {}
variable "engine" {}
variable "env" {}
variable "db_secret_name" {}

# Choose instance class based on environment
locals {
  instance_class = var.env == "prod" ? "db.t3.medium" : "db.t3.micro"
}

# Retrieve secrets from AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_secret" {
  secret_id = var.db_secret_name
}

locals {
  db_credentials = jsondecode(data.aws_secretsmanager_secret_version.db_secret.secret_string)
}

resource "aws_db_instance" "this" {
  identifier             = var.db_name
  engine                 = var.engine
  instance_class         = local.instance_class
  allocated_storage      = 20
  username               = local.db_credentials.username
  password               = local.db_credentials.password
  db_name                = var.db_name
  skip_final_snapshot    = true
  publicly_accessible    = false
  deletion_protection    = false
}
