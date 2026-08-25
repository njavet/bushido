resource "azurerm_container_app_environment" "bushido" {
  name                = "cae-bushido-dev"
  resource_group_name = azurerm_resource_group.bushido.name
  location            = azurerm_resource_group.bushido.location
}

resource "azurerm_container_app" "bushido" {
  name                         = "ca-bushido-dev"
  container_app_environment_id = azurerm_container_app_environment.bushido.id
  resource_group_name          = azurerm_resource_group.bushido.name

  revision_mode = "Single"

  template {
    min_replicas = 1
    max_replicas = 1

    container {
      name   = "bushido-server"
      image  = var.container_image
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "DB_HOST"
        value = azurerm_mssql_server.bushido.fully_qualified_domain_name
      }

      env {
        name  = "DB_NAME"
        value = azurerm_mssql_database.bushido.name
      }

      env {
        name  = "DB_USER"
        value = var.sql_admin_user
      }

      env {
        name        = "DB_PASSWORD"
        secret_name = "db-password"
      }
    }
  }

  secret {
    name  = "db-password"
    value = var.sql_admin_password
  }

  ingress {
    external_enabled = true
    target_port      = 8000

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  identity {
    type = "SystemAssigned"
  }

}