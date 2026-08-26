resource "azurerm_role_assignment" "bushido_acr_pull" {
  scope                = azurerm_container_registry.bushido.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_user_assigned_identity.bushido.principal_id
}

resource "azurerm_user_assigned_identity" "bushido" {
  name                = "id-${local.prefix}"
  resource_group_name = azurerm_resource_group.bushido.name
  location            = azurerm_resource_group.bushido.location
}
