variable "region" {
  default     = "us-east-2"
}

variable "cluster_name" {}
variable "vpc_name" {}

variable "vpc_cidr" {
    default     = "10.10.0.0/16"
}

variable "vpc_private_subnet_cidr" {
    type = list
    default     = ["10.10.1.0/24", "10.10.2.0/24", "10.10.3.0/24"]
}

variable "vpc_public_subnet_cidr" {
    type = list
    default = ["10.10.4.0/24", "10.10.5.0/24", "10.10.6.0/24"]
}