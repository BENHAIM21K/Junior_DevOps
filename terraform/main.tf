variable "db_name" {
  description = "The name of the database"
  type        = string
  default     = "testdb123"
}

variable "engine" {
  description = "The engine for the RDS database"
  type        = string
  default     = "mysql"
}

variable "env" {
  description = "The environment type"
  type        = string
  default     = "dev"
}

variable "db_secret_name" {
  description = "Name of the secret in Secrets Manager containing DB credentials"
  type        = string
  default     = "rds/credentials"
}

variable "vpc_id" {
  description = "VPC ID where RDS will be launched"
  type        = string
  default     = "vpc-05335b2e3d46b1f56"
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
  default     = ["subnet-0a1301c0f647ddc89", "subnet-0ec5fe3110b1231d9"]
}
