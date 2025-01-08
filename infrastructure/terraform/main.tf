terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.32.1"
    }
  }
}

provider "aws" {
  region  = var.region
  default_tags {
    tags = {
      ManagedBy = "Terraform"
    }
  }
}

data "aws_vpc" "vpc" {
  id = "vpc-0e5626dfb9cda94dd"
}


data "aws_subnet" "subnet-1" {
  id = "subnet-0ac06d671ca936ee6"
}

data "aws_subnet" "subnet-2" {
  id = "subnet-0438111a61d1e632e"
}

data "aws_subnet" "subnet-3" {
  id = "subnet-0503cf3f920a1d331"
}

data "aws_subnet" "subnet-4" {
  id = "subnet-055b080b8d82292cf"
}

data "aws_subnet" "subnet-5" {
  id = "subnet-0ae0851c4262d5018"
}

data "aws_subnet" "subnet-6" {
  id = "subnet-0c1a9edd3e7e482e6"
}

