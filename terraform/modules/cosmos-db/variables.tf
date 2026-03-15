variable "app_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "database_name" {
  type    = string
  default = "understand_ms"
}

variable "conversations_container_name" {
  type    = string
  default = "conversations"
}