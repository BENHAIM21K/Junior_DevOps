variable "db_name" {
  type = string
}

variable "engine" {
  type = string
}

variable "env" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "db_secret_name" {
  type = string
  default = "rds/credentials"
}
