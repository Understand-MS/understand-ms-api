variable "app_name" {
  type = string
}

variable "resource_group_name" {
  type        = string
}

variable "container_app_environment_id" {
  type = string
}

variable "container_image" {
  type = string
}

variable "github_username" {
  type = string
}

variable "github_pat" {
  type = string
}

variable "cosmos_url" {
  type        = string
  description = "Cosmos DB account endpoint URL"
}