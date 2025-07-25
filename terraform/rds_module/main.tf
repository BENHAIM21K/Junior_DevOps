
variable "db_name" {
  default = "testdb123"
}

variable "engine" {
  default = "mysql"
}

variable "env" {
  default = "dev"
}

variable "db_secret_name" {
  default = "rds/credentials"
}

module "rds" {
  source           = "./rds_module"
  db_name          = var.db_name
  engine           = var.engine
  env              = var.env
  db_secret_name   = var.db_secret_name
}
