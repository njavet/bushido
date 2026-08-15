output "network_name" {
  description = "Created libvirt network name"
  value       = libvirt_network.bushido.name
}

output "network_id" {
  description = "libvirt network ID"
  value       = libvirt_network.bushido.id
}
