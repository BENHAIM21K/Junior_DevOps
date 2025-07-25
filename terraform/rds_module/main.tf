
variable "db_name" {
  default = "helloWorld"
}

variable "engine" {
  default = "postgres"
}

variable "env" {
  default = "test"
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
