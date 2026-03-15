output "container_app_url" {
  description = "Public URL of the container app"
  value       = "https://${module.api.fqdn}"
}

output "cosmos_endpoint" {
  description = "Cosmos DB account endpoint"
  value       = azurerm_cosmosdb_account.cosmos.endpoint
}