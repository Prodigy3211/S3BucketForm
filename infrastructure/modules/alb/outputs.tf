output "alb_arn" {
  value       = aws_lb.example.arn
  description = "The arn the load balancer"
}

output "alb_arn_suffix" {
  value = aws_lb.example.arn_suffix
  description = "The arn suffix of the load balancer"
}
output "alb_dns" {
  value       = aws_lb.example.dns_name
  description = "The DNS name of the load balancer"
}

output "alb_zone_id" {
  value       = aws_lb.example.zone_id
  description = "The DNS name of the load balancer"
}