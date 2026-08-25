resource "azurerm_role_assignment" "bushido_acr_pull" {
  scope = azurerm_container_registry.bushido.id
  role_definition_name = "AcrPull"
  principal_id = azurerm_container_app.bushido.identity[0].principal_id
}
