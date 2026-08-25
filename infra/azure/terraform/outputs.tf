#-------------------------------------------------------------------------------------
# azure
#-------------------------------------------------------------------------------------
output "sql_server" {
  value = azurerm_mssql_server.bushido.fully_qualified_domain_name
}

output "database_name" {
  value = azurerm_mssql_database.bushido.name
}

output "fastapi_url" {
  value = "https://${azurerm_container_app.bushido.ingress[0].fqdn}"
}