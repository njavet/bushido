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
  default     = null
  nullable    = true
}

variable "postgres_admin_user" {
  type    = string
  default = "bushidoadmin"
}

variable "postgres_admin_password" {
  type      = string
  sensitive = true
}
