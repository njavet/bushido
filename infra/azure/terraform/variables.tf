variable "libvirt_uri" {
  description = "libvirt connection URI"
  type        = string
  default     = "qemu:///system"
}

variable "network_name" {
  description = "Name of the Bushido libvirt network"
  type        = string
  default     = "bushido"
}

variable "network_cidr" {
  description = "CIDR for the Bushido private network"
  type        = string
  default     = "10.20.0.0/24"
}

#-------------------------------------------------------------------------------------
# azure
#-------------------------------------------------------------------------------------
variable "subscription_id" {
  type = string
}

variable "unique_suffix" {
  description = "Makes globally unique Azure resource names"
  type        = string
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