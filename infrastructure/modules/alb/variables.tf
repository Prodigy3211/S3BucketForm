variable "security_group_ids" {
  description = "List of security group IDs to associate with the load balancer"
  type        = list(string)
  default     = []
}


variable "subnet_ids" {
  description = "List of subnet IDs to associate with the load balancer"
  type        = list(string)
  default     = []
}

variable "alb_name" {
    description = "Application loadbalancer name"
    type = string
    default = "example_alb"
}

variable "alb_type" {
    description = "Internal or External Load Balancer"
    type = bool
    default = false
  
}

variable "idle_timeout" {
    description = "The time in seconds that the connection is allowed to be idle"
    type = number
    default = 60
  
}