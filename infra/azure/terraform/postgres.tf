resource "azurerm_postgresql_flexible_server" "bushido" {
  name                = local.postgres_server_name
  resource_group_name = azurerm_resource_group.bushido.name
  location            = azurerm_resource_group.bushido.location

  version = "17"

  administrator_login    = var.postgres_admin_user
  administrator_password = var.postgres_admin_password

  delegated_subnet_id    = azurerm_subnet.postgres.id
  private_dns_zone_id    = azurerm_private_dns_zone.postgres.id

  sku_name   = "B_Standard_B1ms"
  storage_mb = 32768

  backup_retention_days         = 7
  geo_redundant_backup_enabled  = false
  public_network_access_enabled = false

  depends_on = [
    azurerm_private_dns_zone_virtual_network_link.postgres,
  ]
}

resource "azurerm_postgresql_flexible_server_database" "bushido" {
  name      = local.postgres_db_name
  server_id = azurerm_postgresql_flexible_server.bushido.id

  charset   = "UTF8"
  collation = "en_US.utf8"

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "azure" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.bushido.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
