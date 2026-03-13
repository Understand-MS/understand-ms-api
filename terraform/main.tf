resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_log_analytics_workspace" "logs" {
  name                = "${var.app_name}-${var.environment}-logs"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  depends_on = [
    azurerm_resource_group.main
  ]
}

resource "azurerm_container_app_environment" "env" {
  name                       = var.container_app_environment_name
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.logs.id

  sku {
    name     = "Standard" 
    capacity = 1 
  }

  depends_on = [
    azurerm_resource_group.main
  ]
}

module "api" {
  source                        = "./modules/container-app"
  app_name                       = var.app_name
  resource_group_name            = "${var.app_name}-rg"
  container_image                = var.container_image

  depends_on = [
    azurerm_resource_group.main
  ]
}

resource "azurerm_storage_account" "tfstate" {
  name                     = replace(var.resource_group_name, "-", "")
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  depends_on = [
    azurerm_resource_group.main
  ]
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "private"

  depends_on = [
    azurerm_resource_group.main,
    azurerm_storage_account.tfstate
  ]
}