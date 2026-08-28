resource "azurerm_virtual_network" "bushido" {
  name                = "vnet-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.bushido.location
  resource_group_name = azurerm_resource_group.bushido.name

  address_space = ["10.0.0.0/16"]
}


resource "azurerm_subnet" "postgres" {
  name                 = "snet-postgres"
  resource_group_name  = azurerm_resource_group.bushido.name
  virtual_network_name = azurerm_virtual_network.bushido.name

  address_prefixes = ["10.0.1.0/24"]

  delegation {
    name = "postgres"

    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"

      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

resource "azurerm_private_dns_zone" "postgres" {
  name                = "bushido.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.bushido.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgres" {
  name                = "bushido-postgres"
  private_dns_zone_id = azurerm_private_dns_zone.postgres.id
  virtual_network_id  = azurerm_virtual_network.bushido.id
}
