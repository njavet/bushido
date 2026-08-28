locals {
  prefix = "bushido-dev"

  resource_group_name            = "rg-${local.prefix}"
  container_app_environment_name = "cae-${local.prefix}"
  container_app_name             = "ca-${local.prefix}"
  identity_name                  = "id-${local.prefix}"

  acr_name             = "acr${replace(local.prefix, "-", "")}${random_string.suffix.result}"
  postgres_server_name = "psql-${local.prefix}-${random_string.suffix.result}"
  postgres_db_name     = "bushido-db"

  db_host                = azurerm_postgresql_flexible_server.bushido.fqdn
  db_name                = azurerm_postgresql_flexible_server_database.bushido.name
  db_username            = "${var.postgres_admin_user}@${azurerm_postgresql_flexible_server.bushido.name}"
  db_username_urlencoded = replace(local.db_username, "@", "%40")
  db_password_urlencoded = urlencode(var.postgres_admin_password)
  db_url                 = "postgresql+psycopg://${local.db_username_urlencoded}:${local.db_password_urlencoded}@${local.db_host}:5432/${local.db_name}?sslmode=require"

  container_image = coalesce(
    var.container_image,
    "${azurerm_container_registry.bushido.login_server}/bushido-server:latest",
  )
}
