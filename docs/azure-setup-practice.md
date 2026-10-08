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
  -n <name>
```

* container app
```
az containerapp env create \
  -g <name> \
  -n <name> \
  -l <loc>
```


* acr image
```
az acr login -n <name> -g <name>

docker build \
-f packages/citadel/Dockerfile \
-t acrbushidonjg.azurecr.io/citadel:latest .

docker push acrbushidonjg.azurecr.io/citadel:latest
```

* managed identity
```
az identity create \
  -g $RG \
  -n id-bushido-prod \
  -l $LOC

IDENTITY_PRINCIPAL_ID=$(az identity show \
  -g $RG \
  -n id-bushido-prod \
  --query principalId -o tsv)

ACR_ID=$(az acr show \
  -g $RG \
  -n acrbushidonjg \
  --query id -o tsv)

az role assignment create \
  --assignee-object-id $IDENTITY_PRINCIPAL_ID \
  --assignee-principal-type ServicePrincipal \
  --role AcrPull \
  --scope $ACR_ID
```

```
az containerapp create \
  -g $RG \
  -n ca-bushido-prod \
  --environment cae-bushido-prod \
  --image acrbushidonjg.azurecr.io/citadel:latest \
  --registry-server acrbushidonjg.azurecr.io \
  --registry-identity "$IDENTITY_ID" \
  --user-assigned "$IDENTITY_ID" \
  --target-port 8000 \
  --ingress external \
```

* container app key vault
```
KV_ID=$(az keyvault show \
  -g $RG \
  -n kv-bushido-njg \
  --query id -o tsv)

az role assignment create \
  --assignee-object-id $IDENTITY_PRINCIPAL_ID \
  --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" \
  --scope $KV_ID

SECRET_URI=$(az keyvault secret show \
  --vault-name kv-bushido-njg \
  --name postgres-password \
  --query id -o tsv)

az containerapp secret set \
  -g $RG \
  -n ca-bushido-prod \
  --secrets \
  "postgres-password=keyvaultref:$SECRET_URI,identityref:$IDENTITY_ID"

az containerapp update \
  -g $RG \
  -n ca-bushido-prod \
  --set-env-vars \
  "POSTGRES_PASSWORD=secretref:postgres-password"
```

* postgres conn
```
PG_HOST=$(az postgres flexible-server show \
  -g $RG \
  -n pg-bushido-njg \
  --query fullyQualifiedDomainName -o tsv)

az containerapp update \
  -g $RG \
  -n ca-bushido-prod \
  --set-env-vars \
  "POSTGRES_HOST=$PG_HOST" \
  "POSTGRES_DB=bushido-db" \
  "POSTGRES_USER=bushido"
```

* vnet
```
az network vnet create \
  -g $RG \
  -n vnet-bushido-prod \
  -l $LOC \
  --address-prefixes 10.0.0.0/16


az network vnet subnet create \
  -g $RG \
  --vnet-name vnet-bushido-prod \
  -n snet-containerapps \
  --address-prefixes 10.0.1.0/23

az network vnet subnet create \
  -g $RG \
  --vnet-name vnet-bushido-prod \
  -n snet-postgres \
  --address-prefixes 10.0.4.0/24 \
  --delegations Microsoft.DBforPostgreSQL/flexibleServers

```
postgres
```
az postgres flexible-server create \
  -g $RG \
  -n pg-bushido-njg \
  -l $LOC \
  --admin-user bushido \
  --admin-password "$PG_PASSWORD" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 16 \
  --vnet vnet-bushido-prod \
  --subnet snet-postgres

az postgres flexible-server db create \
  -g $RG \
  -s pg-bushido-njg \
  -n bushido-db

```
