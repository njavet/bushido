resource "azurerm_resource_group" "bushido" {
  name     = "rg-${local.prefix}"
  location = var.location
}
