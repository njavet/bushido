
* resource group creation:
```
az group create --name <name> --location <loc>
```

* container registry
```
az acr create --resource-group <name> --name <name> --sku <sku> --location <loc>
```

* key vault
```
az keyvault create -g <name> -n <name> -l <loc> --enable-rbac-authorization true
```

* assign permission
```
MY_ID=$(az ad signed-in-user show --query id -o tsv)

KV_ID=$(az keyvault show \
  -g $RG \
  -n <name> \
  --query id -o tsv)

az role assignment create \
  --assignee $MY_ID \
  --role "Key Vault Secrets Officer" \
  --scope $KV_ID
```

* postgres password
```

PG_PASSWORD=$(openssl rand -base64 32)

az keyvault secret set \
  --vault-name <name> \
  --name postgres-password \
  --value "$PG_PASSWORD"
```

* postgres flex server
```
az postgres flexible-server create \
  -g <name> \
  -n <name> \
  -l $LOC \
  --admin-user <name> \
  --admin-password "$PG_PASSWORD" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 16
```

* db
```
az postgres flexible-server db create \
  -g <name> \
  -s <name> \
  -d <name>
```

* container app
```
az containerapp env create \
  -g <name> \
  -n <name> \
  -l <loc>
```


