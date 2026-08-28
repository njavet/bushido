resource "azurerm_container_app_environment" "bushido" {
  name                = local.container_app_environment_name
  location            = azurerm_resource_group.bushido.location
  resource_group_name = azurerm_resource_group.bushido.name

  infrastructure_subnet_id = azurerm_subnet.container_apps.id
}

resource "azurerm_container_app" "bushido" {
  name                         = local.container_app_name
  container_app_environment_id = azurerm_container_app_environment.bushido.id
  resource_group_name          = azurerm_resource_group.bushido.name

  revision_mode = "Single"

  secret {
    name  = "postgres-url"
    value = local.db_url
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "bushido-server"
      image  = local.container_image
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "DB_BACKEND"
        value = "postgres"
      }

      env {
        name        = "POSTGRES_URL"
        secret_name = "postgres-url"
      }
    }
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
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.bushido.id,
    ]
  }

  registry {
    server   = azurerm_container_registry.bushido.login_server
    identity = azurerm_user_assigned_identity.bushido.id
  }
}