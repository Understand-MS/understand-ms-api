data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                = "${var.app_name}-${var.environment}-kv"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id

  sku_name = "standard"
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

module "cosmos" {
  source = "./modules/cosmos-db"

  app_name            = var.app_name
  environment         = var.environment
  resource_group_name = data.azurerm_resource_group.main.name
  location            = data.azurerm_resource_group.main.location
}

module "api" {
  source = "./modules/container-app"

  app_name                     = var.app_name
  resource_group_name          = data.azurerm_resource_group.main.name
  container_app_environment_id = azurerm_container_app_environment.env.id
  container_image              = var.container_image
  github_username              = var.github_username
  github_pat                   = var.github_pat
  cosmos_url                   = module.cosmos.endpoint
}

resource "azurerm_cosmosdb_sql_role_assignment" "api_data_contributor" {
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = module.cosmos.account_name
  role_definition_id  = "${module.cosmos.account_id}/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002"
  principal_id        = module.api.principal_id
  scope               = module.cosmos.account_id
}