output "postgres_server" {
  value = azurerm_postgresql_flexible_server.bushido.fqdn
}

output "database_name" {
  value = azurerm_postgresql_flexible_server_database.bushido.name
}

output "fastapi_url" {
  value = "https://${azurerm_container_app.bushido.ingress[0].fqdn}"
}

output "acr_login_server" {
  value = azurerm_container_registry.bushido.login_server
}
