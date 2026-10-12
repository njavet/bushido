### rg
```
export RG=rg-bushido-az104-lab
export LOC=switzerlandnorth

az group create \
  -n $RG \
  -l $LOC
```
### spoke / application vnet
```
az network vnet create \
  -g $RG \
  -n vnet-bushido-app \
  -l $LOC \
  --address-prefixes 10.10.0.0/16
```
### frontend
```
az network vnet subnet create \
  -g $RG \
  --vnet-name vnet-bushido-app \
  -n snet-web \
  --address-prefixes 10.10.1.0/24
```
### backend
```
az network vnet subnet create \
  -g $RG \
  --vnet-name vnet-bushido-app \
  -n snet-api \
  --address-prefixes 10.10.2.0/24
```
### hub
```
az network vnet create \
  -g $RG \
  -n vnet-bushido-hub \
  -l $LOC \
  --address-prefixes 10.20.0.0/16

az network vnet subnet create \
  -g $RG \
  --vnet-name vnet-bushido-hub \
  -n snet-management \
  --address-prefixes 10.20.1.0/24
```

### peer app and hub vnet
```
APP_VNET_ID=$(az network vnet show \
  -g $RG \
  -n vnet-bushido-app \
  --query id -o tsv)

HUB_VNET_ID=$(az network vnet show \
  -g $RG \
  -n vnet-bushido-hub \
  --query id -o tsv)

az network vnet peering create \
  -g $RG \
  --vnet-name vnet-bushido-app \
  -n peer-app-to-hub \
  --remote-vnet $HUB_VNET_ID \
  --allow-vnet-access

az network vnet peering create \
  -g $RG \
  --vnet-name vnet-bushido-hub \
  -n peer-hub-to-app \
  --remote-vnet $APP_VNET_ID \
  --allow-vnet-access
```

### application security groups
```
az network asg create \
  -g $RG \
  -n asg-bushido-web \
  -l $LOC

az network asg create \
  -g $RG \
  -n asg-bushido-api \
  -l $LOC

az network asg create \
  -g $RG \
  -n asg-bushido-admin \
  -l $LOC
```

### network security groups
```
az network nsg create \
  -g $RG \
  -n nsg-bushido-web \
  -l $LOC

az network nsg create \
  -g $RG \
  -n nsg-bushido-api \
  -l $LOC

az network nsg create \
  -g $RG \
  -n nsg-bushido-management \
  -l $LOC

az network vnet subnet update \
  -g $RG \
  --vnet-name vnet-bushido-app \
  -n snet-web \
  --network-security-group nsg-bushido-web

az network vnet subnet update \
  -g $RG \
  --vnet-name vnet-bushido-app \
  -n snet-api \
  --network-security-group nsg-bushido-api

az network vnet subnet update \
  -g $RG \
  --vnet-name vnet-bushido-hub \
  -n snet-management \
  --network-security-group nsg-bushido-management
```

### vm

