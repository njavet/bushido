locals {
  prefix = "bushido-dev"
}

locals {
  db_url = "mssql+pyodbc://${var.sql_admin_user}:${var.sql_admin_password}@${azurerm_mssql_server.bushido.fully_qualified_domain_name}:1433/${azurerm_mssql_database.bushido.name}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes"
}
