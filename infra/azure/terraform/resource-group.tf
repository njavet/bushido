resource "azurerm_resource_group" "bushido" {
  name     = local.resource_group_name
  location = var.location
}
