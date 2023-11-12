output "helpful_ai_server_eip" {
  value       = aws_eip.helpful_ai_server.public_ip
  description = "Elastic IP of Helpful AI server."
}