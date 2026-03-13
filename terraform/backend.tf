terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.75"
    }
  }

  # backend "azurerm" {
  #   resource_group_name  = "understand-ms-rg"
  #   storage_account_name = "understandmstfstateaccount"
  #   container_name       = "tfstate"
  #   key                  = "terraform.tfstate"
  # }
}

provider "azurerm" {
  features {}
}