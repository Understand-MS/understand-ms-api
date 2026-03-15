output "container_app_url" {
  description = "Public URL of the container app"
  value       = "https://${module.api.fqdn}"
}

output "cosmos_endpoint" {
  description = "Cosmos DB account endpoint"
  value       = module.cosmos.endpoint
}