variable "region" {
  default = "us-east-1"
}

variable "env" {
  description = "Environment"
  type        = string
}

variable "ecr_repo" {
  description = "ECR Repository"
  type        = string
}

variable "desired_count" {
  description = "Desired Count"
  type        = number
  
}

variable "cpu" {
  description = "CPU"
  type        = number
}

variable "cpu_str" {
  description = "CPU"
  type        = string
}

variable "memory" {
  description = "Memory"
  type        = number
}

variable "memory_str" {
  description = "Memory"
  type        = string
}

variable "domain_name" {
  description = "Domain Name"
  type        = string
}

variable "zone_id" {
  description = "Zone ID"
  type        = string
}

variable "certificate_arn" {
  description = "Certificate ARN"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs"
  type        = list(string)
  default = ["subnet-0ac06d671ca936ee6", "subnet-0ac06d671ca936ee6", "subnet-0503cf3f920a1d331", "subnet-055b080b8d82292cf" , "subnet-0ae0851c4262d5018" ,"subnet-0c1a9edd3e7e482e6"]
  
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
  default = "vpc-0e5626dfb9cda94dd"
  
}

variable "vpc_cidr_block" {
  description = "VPC CIDR Block"
  type        = string
  default = "172.31.0.0/16"
  
}