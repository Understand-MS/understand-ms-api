terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.75"
    }
  }

  backend "azurerm" {
    resource_group_name  = var.resource_group_name
    storage_account_name = "${var.app_name}tfstateaccount"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}