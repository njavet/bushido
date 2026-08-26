resource "azurerm_mssql_server" "bushido" {
  name                = "sql-bushido-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.bushido.name
  location            = azurerm_resource_group.bushido.location

  version = "12.0"

  administrator_login          = var.sql_admin_user
  administrator_login_password = var.sql_admin_password

  # first learning version
  public_network_access_enabled = true
}

resource "azurerm_mssql_database" "bushido" {
  name      = "bushido-db"
  server_id = azurerm_mssql_server.bushido.id

  sku_name = "Basic"
}

resource "azurerm_mssql_firewall_rule" "azure" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.bushido.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
