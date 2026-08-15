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
