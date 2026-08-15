resource "libvirt_network" "bushido" {
  name = var.network_name

  forward = {
    mode = "nat"
  }

  ips = [
    {
      address = var.network_cidr
      family  = "ipv4"

      dhcp = {
        enabled = true
      }
    }
  ]
}
