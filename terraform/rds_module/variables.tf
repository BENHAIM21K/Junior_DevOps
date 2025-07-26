variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "engine" {
  description = "Database engine (e.g., mysql, postgres)"
  type        = string
}

variable "env" {
  description = "Environment (e.g., test, prod)"
  type        = string
}

variable "db_secret_name" {
  description = "Name of the secret in AWS Secrets Manager"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for RDS"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for RDS subnet group"
  type        = list(string)
}

variable "instance_class" {
  description = "Instance class for RDS"
  type        = string
}
