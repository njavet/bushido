### 0. define shell variables:
```
export LOC=switzerlandnorth
export RG=rg-bushido-prod
export VNET=vnet-bushido-prod
export SNET_APP=snet-app-prod
export SNET_DB=snet-db-prod
export CAE=cae-bushido-prod
export CA=ca-bushido-api-prod
export KV=kv-bushido-prod-njg
export ACR=acrbushidoprodnjg
export PG=psql-bushido-prod-njg
export ID=id-bushido-prod
```
### 1. resource group creation:
```
az group create --name $RG --location $LOC
```

### 2. create vnet
```aiignore
az network vnet create \
  -g $RG \
  -n $VNET \
  -l $LOC \
  --address-prefixes 10.0.0.0/16
```

### 3. container app subnet
```aiignore
az network vnet subnet create \
  -g $RG \
  --vnet-name $VNET \
  -n $SNET_APP \
  --address-prefixes 10.0.0.0/23
```

### 4. postgres subnet
```aiignore
az network vnet subnet create \
  -g $RG \
  --vnet-name $VNET \
  -n $SNET_DB \
  --address-prefixes 10.0.2.0/24 \
  --delegations Microsoft.DBforPostgreSQL/flexibleServers
```

### 5. private dns zone
```aiignore
export PDNS=bushido.postgres.database.azure.com

az network private-dns zone create \
  -g $RG \
  -n $PDNS
  
az network private-dns link vnet create \
  -g $RG \
  -n pdnslink-bushido-prod \
  -z $PDNS \
  -v $VNET \
  -e false
  
```

### 6. postgres
```aiignore
export PG_PASSWORD=$(openssl rand -base64 32)
export PG=psql-bushido-prod-njg

az postgres flexible-server create \
  -g $RG \
  -n $PG \
  -l $LOC \
  --admin-user bushido \
  --admin-password "$PG_PASSWORD" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 16 \
  --vnet $VNET \
  --subnet $SNET_DB \
  --private-dns-zone $PDNS
  
az postgres flexible-server db create \
  -g $RG \
  -s $PG \
  -n bushido-db 
```

### 7. container registry
```aiignore
az acr create \
  -g $RG \
  -n $ACR \
  -l $LOC \
  --sku Basic
```

### 8. keyvault
```aiignore
az keyvault create \
  -g $RG \
  -n $KV \
  -l $LOC \
  --enable-rbac-authorization true
```
  
### 9. managed identity
```aiignore
az identity create \
  -g $RG \
  -n $ID \
  -l $LOC
  
export ID_PRINCIPAL=$(az identity show \
  -g $RG \
  -n $ID \
  --query principalId -o tsv)
```

### 10. rbac
```aiignore
export ACR_ID=$(az acr show \
  -g $RG \
  -n $ACR \
  --query id -o tsv)

az role assignment create \
  --assignee-object-id $ID_PRINCIPAL \
  --assignee-principal-type ServicePrincipal \
  --role AcrPull \
  --scope $ACR_ID
  
  
 export KV_ID=$(az keyvault show \
  -g $RG \
  -n $KV \
  --query id -o tsv)

az role assignment create \
  --assignee-object-id $ID_PRINCIPAL \
  --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" \
  --scope $KV_ID
  
export MY_ID=$(az ad signed-in-user show \
  --query id -o tsv)

az role assignment create \
  --assignee-object-id $MY_ID \
  --assignee-principal-type User \
  --role "Key Vault Secrets Officer" \
  --scope $KV_ID
```

### 11. postgres keyvault
```aiignore
az keyvault secret set \
  --vault-name $KV \
  --name postgres-password \
  --value "$PG_PASSWORD"
  
  
export SECRET_URI=$(az keyvault secret show \
  --vault-name $KV \
  --name postgres-password \
  --query id -o tsv)
```

### 12. container app env
```aiignore
export APP_SUBNET_ID=$(az network vnet subnet show \
  -g $RG \
  --vnet-name $VNET \
  -n $SNET_APP \
  --query id -o tsv)
  
az network vnet subnet update \
  -g $RG \
  --vnet-name $VNET \
  -n $SNET_APP \
  --delegations Microsoft.App/environments
export CAE=cae-bushido-prod

az containerapp env create \
  -g $RG \
  -n $CAE \
  -l $LOC \
  --infrastructure-subnet-resource-id "$APP_SUBNET_ID"
```

