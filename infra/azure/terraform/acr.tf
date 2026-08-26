resource "azurerm_container_registry" "bushido" {
  name = "acrbushido"
  resource_group_name = azurerm_resource_group.bushido.name
  location = azurerm_resource_group.bushido.location

  sku = "Basic"
  admin_enabled = false
}