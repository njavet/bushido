variable "subscription_id" {
  type = string
}

variable "location" {
    type    = string
    default = "Switzerland North"
}

variable "container_image" {
  description = "Docker image accessible by Azure Container Apps"
  type        = string
}

variable "sql_admin_user" {
  type    = string
  default = "bushidoadmin"
}

variable "sql_admin_password" {
  type      = string
  sensitive = true
}