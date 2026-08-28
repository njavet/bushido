variable "subscription_id" {
  type = string
}

variable "project_name" {
  type    = string
  default = "bushido"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "location" {
  type = object({
    token     = string
    full_name = string
  })
  default = {
    token     = "swn"
    full_name = "Switzerland North"
  }
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
