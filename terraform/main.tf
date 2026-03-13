data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

resource "azurerm_log_analytics_workspace" "logs" {
  name                = "${var.app_name}-${var.environment}-logs"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "env" {
  name                       = var.container_app_environment_name
  location                   = data.azurerm_resource_group.main.location
  resource_group_name        = data.azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.logs.id
}

module "api" {
  source = "./modules/container-app"

  app_name                     = var.app_name
  resource_group_name          = data.azurerm_resource_group.main.name
  container_app_environment_id = azurerm_container_app_environment.env.id
  container_image              = var.container_image
}