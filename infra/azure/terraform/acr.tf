resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

resource "azurerm_container_registry" "bushido" {
  name                = "acrbushido${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.bushido.name
  location            = azurerm_resource_group.bushido.location
  sku                 = "Basic"
  admin_enabled       = false
}