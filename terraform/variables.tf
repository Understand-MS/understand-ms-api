variable "environment" {
  description = "Environment to deploy (dev/prod)"
  type        = string
}

variable "resource_group_name" {
  type        = string
  default     = "understand-ms-rg"
}

variable "location" {
  type        = string
  description = "Azure region"
  default     = "westeurope"
}

variable "app_name" {
  type        = string
  description = "Container App name"
}

variable "container_image" {
  type        = string
  description = "Docker image for the Container App"
}