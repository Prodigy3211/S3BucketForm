resource "aws_lb" "example" {
  name               = var.alb_name
  load_balancer_type = "application"
  subnets            = var.subnet_ids
  security_groups    = var.security_group_ids
  internal = var.alb_type
  idle_timeout = var.idle_timeout
}
