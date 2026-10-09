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

### 13. image / acr
```aiignore
az acr login -n $ACR -g $RG

docker build \
  -f packages/citadel/Dockerfile \
  -t $ACR.azurecr.io/citadel:latest .
  
docker push $ACR.azurecr.io/citadel:latest
```

### 14. container app
```aiignore
export ID_RESOURCE=$(az identity show \
  -g $RG \
  -n $ID \
  --query id -o tsv)

az containerapp create \
  -g $RG \
  -n $CA \
  --environment $CAE \
  --image $ACR.azurecr.io/citadel:latest \
  --registry-server $ACR.azurecr.io \
  --registry-identity "$ID_RESOURCE" \
  --user-assigned "$ID_RESOURCE" \
  --target-port 8000 \
  --ingress external
```

### 15. kv and postgres conf
```aiignore
az containerapp secret set \
  -g $RG \
  -n $CA \
  --secrets \
  "postgres-password=keyvaultref:$SECRET_URI,identityref:$ID_RESOURCE"
  
 export PG_HOST=$(az postgres flexible-server show \
  -g $RG \
  -n $PG \
  --query fullyQualifiedDomainName -o tsv) 
  
 az containerapp update \
  -g $RG \
  -n $CA \
  --set-env-vars \
  "POSTGRES_HOST=$PG_HOST" \
  "POSTGRES_DATABASE=bushido-db" \
  "POSTGRES_USER=bushido" \
  "POSTGRES_PASSWORD=secretref:postgres-password" 
```

### 16. storage account
```aiignore
export STORAGE=stbushidoprodnjg

az storage account create \
  -g $RG \
  -n $STORAGE \
  -l $LOC \
  --sku Standard_LRS \
  --kind StorageV2 \
  --https-only true \
  --min-tls-version TLS1_2
  
az storage container create \
  --account-name $STORAGE \
  --name videos \
  --auth-mode login

az storage container create \
  --account-name $STORAGE \
  --name backups \
  --auth-mode login
  
az storage queue create \
  --account-name $STORAGE \
  --name ai-jobs \
  --auth-mode login
  
export SNET_PE=snet-private-endpoints-prod

az network vnet subnet create \
  -g $RG \
  --vnet-name $VNET \
  -n $SNET_PE \
  --address-prefixes 10.0.3.0/24
  
export PE_SUBNET_ID=$(az network vnet subnet show \
  -g $RG \
  --vnet-name $VNET \
  -n $SNET_PE \
  --query id -o tsv)

export STORAGE_ID=$(az storage account show \
  -g $RG \
  -n $STORAGE \
  --query id -o tsv)
  
az network private-endpoint create \
  -g $RG \
  -n pe-bushido-blob-prod \
  --subnet $PE_SUBNET_ID \
  --private-connection-resource-id $STORAGE_ID \
  --group-id blob \
  --connection-name pec-bushido-blob-prod
  
export BLOB_PDNS=privatelink.blob.core.windows.net

az network private-dns zone create \
  -g $RG \
  -n $BLOB_PDNS
  
az network private-dns link vnet create \
  -g $RG \
  -n pdnslink-blob-prod \
  -z $BLOB_PDNS \
  -v $VNET \
  -e false
  
az network private-endpoint dns-zone-group create \
  -g $RG \
  --endpoint-name pe-bushido-blob-prod \
  -n dzg-blob-prod \
  --private-dns-zone $BLOB_PDNS \
  --zone-name blob
```

### 17. disable public access
```aiignore
az storage account update \
  -g $RG \
  -n $STORAGE \
  --public-network-access Disabled
```

### 18. frontend
```aiignore
export WEB=stbushidowebprodnjg

az storage account create \
  -g $RG \
  -n $WEB \
  -l $LOC \
  --sku Standard_LRS \
  --kind StorageV2 \
  --https-only true
  
export WEB_ID=$(az storage account show \
  -g $RG \
  -n $WEB \
  --query id -o tsv)
  
 az role assignment create \
  --assignee-object-id $MY_ID \
  --assignee-principal-type User \
  --role "Storage Blob Data Contributor" \
  --scope $WEB_ID 
  
 az storage blob service-properties update \
  --account-name $WEB \
  --static-website \
  --index-document index.html \
  --404-document index.html 
  
az storage blob upload \
  --account-name $WEB \
  --container-name '$web' \
  --name index.html \
  --file index.html \
  --auth-mode login \
  --overwrite

az storage blob upload \
  --account-name $WEB \
  --container-name '$web' \
  --name elm.js \
  --file elm.js \
  --auth-mode login \
  --overwrite
  
export WEB_URL=$(az storage account show \
  -g $RG \
  -n $WEB \
  --query primaryEndpoints.web \
  -o tsv)

export API_FQDN=$(az containerapp show \
  -g $RG \
  -n $CA \
  --query properties.configuration.ingress.fqdn \
  -o tsv)

```

### 19. dns
```aiignore
az containerapp hostname add \
  -g $RG \
  -n $CA \
  --hostname api.bushido.nj-cyb.org
  
az containerapp hostname bind \
  -g $RG \
  -n $CA \
  --hostname api.bushido.nj-cyb.org \
  --environment $CAE \
  --validation-method CNAME
```

### 20. frontdoor
```aiignore
export AFD_PROFILE=afd-bushido-prod
export AFD_ENDPOINT=bushido-prod-njg
export AFD_ORIGIN_GROUP=og-bushido-web-prod
export AFD_ORIGIN=origin-bushido-web-prod
export AFD_ROUTE=route-bushido-web-prod

az afd profile create \
  -g $RG \
  -n $AFD_PROFILE \
  --sku Standard_AzureFrontDoor
  
 az afd endpoint create \
  -g $RG \
  --profile-name $AFD_PROFILE \
  -n $AFD_ENDPOINT \
  --enabled-state Enabled 
  
  export WEB_HOST=$(az storage account show \
  -g $RG \
  -n $WEB \
  --query 'primaryEndpoints.web' \
  -o tsv | sed -E 's#^https?://##; s#/$##')

echo $WEB_HOST
az afd origin-group create \
  -g $RG \
  --profile-name $AFD_PROFILE \
  -n $AFD_ORIGIN_GROUP \
  --probe-request-type GET \
  --probe-protocol Https \
  --probe-interval-in-seconds 120 \
  --probe-path / \
  --sample-size 4 \
  --successful-samples-required 3 \
  --additional-latency-in-milliseconds 50

az afd origin create \
  -g $RG \
  --profile-name $AFD_PROFILE \
  --origin-group-name $AFD_ORIGIN_GROUP \
  -n $AFD_ORIGIN \
  --host-name $WEB_HOST \
  --origin-host-header $WEB_HOST \
  --http-port 80 \
  --https-port 443 \
  --priority 1 \
  --weight 1000 \
  --enabled-state Enabled
  
 az afd route create \
  -g $RG \
  --profile-name $AFD_PROFILE \
  --endpoint-name $AFD_ENDPOINT \
  -n $AFD_ROUTE \
  --origin-group $AFD_ORIGIN_GROUP \
  --supported-protocols Http Https \
  --patterns-to-match '/*' \
  --forwarding-protocol HttpsOnly \
  --https-redirect Enabled \
  --link-to-default-domain Enabled 
  
 az afd endpoint show \
  -g $RG \
  --profile-name $AFD_PROFILE \
  -n $AFD_ENDPOINT \
  --query hostName \
  -o tsv 
  
  
 export AFD_HOST=$(az afd endpoint show \
  -g $RG \
  --profile-name $AFD_PROFILE \
  -n $AFD_ENDPOINT \
  --query hostName -o tsv)

echo $AFD_HOST 

az afd custom-domain create \
  -g $RG \
  --profile-name $AFD_PROFILE \
  -n bushido-prod \
  --host-name bushido.nj-cyb.org \
  --certificate-type ManagedCertificate \
  --minimum-tls-version TLS12
  
 export DOMAIN_ID=$(az afd custom-domain show \
  -g $RG \
  --profile-name $AFD_PROFILE \
  -n bushido-prod \
  --query id -o tsv) 
  
 az afd route update \
  -g $RG \
  --profile-name $AFD_PROFILE \
  --endpoint-name $AFD_ENDPOINT \
  -n $AFD_ROUTE \
  --formatted-custom-domains "[{id:$DOMAIN_ID}]" 

az afd custom-domain show \
 -g $RG \
 --profile-name $AFD_PROFILE \
 -n bushido-dev \
 --query validationProperties  \
 -o yaml
 

```

### alembic 
```
export JOB=job-bushido-migrate-prod
export IMAGE="$ACR.azurecr.io/citadel:latest"

az containerapp job create \
  -g $RG \
  -n $JOB \
  --environment $CAE \
  --trigger-type Manual \
  --replica-timeout 300 \
  --replica-retry-limit 1 \
  --image "$IMAGE" \
  --registry-server "$ACR.azurecr.io" \
  --registry-identity "$ID_RESOURCE" \
  --user-assigned "$ID_RESOURCE" \
  --command "uv" \
  --args "run" "alembic" "upgrade" "head"
  
 az containerapp job secret set \
  -g $RG \
  -n $JOB \
  --secrets \
  "postgres-password=keyvaultref:$SECRET_URI,identityref:$ID_RESOURCE"
  
  az containerapp job update \
  -g $RG \
  -n $JOB \
  --set-env-vars \
  "POSTGRES_HOST=$PG_HOST" \
  "POSTGRES_DATABASE=bushido-db" \
  "POSTGRES_USER=bushido" \
  "POSTGRES_PASSWORD=secretref:postgres-password"
```
manual run:
```aiignore
az containerapp job start \
  -g $RG \
  -n $JOB
  
 az containerapp job execution list \
  -g $RG \
  -n $JOB \
  -o table
```

### prod architecture

bushido.nj-cyb.org
        │
        ▼
   Front Door
        │
        ▼
Storage static website
        │
        ▼
   Elm browser app
        │ HTTPS
        ▼
api.bushido.nj-cyb.org
        │
        ▼
 Container Apps
   │         │
   │         └── Managed Identity
   │               ├── ACR
   │               └── Key Vault
   │
   ▼
Private DNS
   │
   ▼
Private PostgreSQL
