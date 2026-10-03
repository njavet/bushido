# GitHub Actions → Azure with OIDC

This note documents how to let a GitHub Actions workflow deploy to Azure
**without storing an Azure password or client secret in GitHub**.

The example assumes:

-   GitHub repository: `YOUR_GITHUB_USER/YOUR_REPO`
-   GitHub environment: `dev`
-   Azure resource group: `YOUR_RESOURCE_GROUP`
-   Entra application name: `github-YOUR_APP`
-   The Azure CLI is installed and you are already logged in to the
    correct tenant/subscription.

Replace the example names with your own values.

## 1. Mental model

There are several different objects involved:

``` text
GitHub Actions
    |
    | GitHub issues a short-lived OIDC token
    v
Microsoft Entra ID
    |
    | federated credential trusts a particular
    | GitHub repository/environment
    v
App Registration
    |
    | has an Application (client) ID
    v
Service Principal
    |
    | receives Azure RBAC permissions
    v
Azure resource group
```

The important distinction is:

-   **App registration**: definition/identity of the application in
    Entra ID.
-   **Service principal**: the tenant-local identity that actually
    receives permissions.
-   **Federated credential**: tells Entra which GitHub identity is
    allowed to authenticate as this application.
-   **RBAC role assignment**: tells Azure what the service principal is
    allowed to do.
-   **OIDC**: lets GitHub authenticate without a long-lived client
    secret.

## 2. Verify the current Azure context

Before creating anything, check which subscription and tenant the CLI is
using:

``` bash
az account show \
  --query '{subscription:name, subscriptionId:id, tenantId:tenantId}' \
  -o json
```

This matters because Entra applications and service principals are
tenant-specific, while RBAC assignments apply to Azure scopes such as
subscriptions and resource groups.

Store the IDs for the commands below:

``` bash
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
TENANT_ID=$(az account show --query tenantId -o tsv)

echo "$SUBSCRIPTION_ID"
echo "$TENANT_ID"
```

## 3. Define names

``` bash
APP_NAME="github-YOUR_APP"
RESOURCE_GROUP="YOUR_RESOURCE_GROUP"
GITHUB_REPOSITORY="YOUR_GITHUB_USER/YOUR_REPO"
GITHUB_ENVIRONMENT="dev"
```

These are ordinary names, not credentials.

## 4. Create the Entra App Registration

``` bash
az ad app create \
  --display-name "$APP_NAME"
```

This creates an **application object** in Microsoft Entra ID.

Get its IDs:

``` bash
CLIENT_ID=$(az ad app list \
  --display-name "$APP_NAME" \
  --query '[0].appId' \
  -o tsv)

APP_OBJECT_ID=$(az ad app list \
  --display-name "$APP_NAME" \
  --query '[0].id' \
  -o tsv)

echo "Client ID: $CLIENT_ID"
echo "Application Object ID: $APP_OBJECT_ID"
```

Do not confuse these:

``` text
appId  = Application (client) ID
id     = Object ID of the App Registration
```

The **client ID is an identifier, not a password**.

## 5. Create the Service Principal

``` bash
az ad sp create \
  --id "$CLIENT_ID"
```

Why?

The App Registration defines the application. The **service principal**
is the application's identity inside this Entra tenant and is the object
to which Azure permissions are assigned.

Get its Object ID:

``` bash
SP_OBJECT_ID=$(az ad sp show \
  --id "$CLIENT_ID" \
  --query id \
  -o tsv)

echo "$SP_OBJECT_ID"
```

Again:

``` text
CLIENT_ID       -> identifies the application
APP_OBJECT_ID   -> identifies the App Registration object
SP_OBJECT_ID    -> identifies the Service Principal object
```

## 6. Give the Service Principal Azure permissions

For a deployment application, prefer granting access only to the
resource group it needs rather than the entire subscription.

``` bash
az role assignment create \
  --assignee-object-id "$SP_OBJECT_ID" \
  --assignee-principal-type ServicePrincipal \
  --role Contributor \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP"
```

This means:

``` text
principal = GitHub application's service principal
role      = Contributor
scope     = only this resource group
```

`Contributor` can create/change/delete resources at that scope, but
cannot generally grant Azure RBAC roles to other identities.

Inspect the assignment:

``` bash
az role assignment list \
  --assignee-object-id "$SP_OBJECT_ID" \
  --all \
  -o table
```

## 7. Add the GitHub OIDC federated credential

The GitHub workflow will run using the `dev` GitHub Environment.

The corresponding GitHub OIDC subject is:

``` text
repo:YOUR_GITHUB_USER/YOUR_REPO:environment:dev
```

Create the federated credential:

``` bash
az ad app federated-credential create \
  --id "$APP_OBJECT_ID" \
  --parameters "{
    \"name\": \"github-dev\",
    \"issuer\": \"https://token.actions.githubusercontent.com\",
    \"subject\": \"repo:${GITHUB_REPOSITORY}:environment:${GITHUB_ENVIRONMENT}\",
    \"audiences\": [
      \"api://AzureADTokenExchange\"
    ]
  }"
```

This establishes the trust relationship:

``` text
Entra application:
    github-YOUR_APP

trusts tokens issued by:
    https://token.actions.githubusercontent.com

but only when subject is:
    repo:YOUR_GITHUB_USER/YOUR_REPO:environment:dev
```

A token from some unrelated GitHub repository therefore cannot
authenticate as this application.

Inspect the credential:

``` bash
az ad app federated-credential list \
  --id "$APP_OBJECT_ID" \
  -o table
```

## 8. Configure GitHub

Create these GitHub Environment variables/secrets for the `dev`
environment:

``` text
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

Get their values:

``` bash
echo "AZURE_CLIENT_ID=$CLIENT_ID"
echo "AZURE_TENANT_ID=$TENANT_ID"
echo "AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID"
```

These three values are **identifiers, not authentication secrets**. It
is still reasonable to keep deployment configuration in GitHub
Environment variables/secrets, but leaking one of these IDs does not
give someone credentials to your Azure account.

There is deliberately **no `AZURE_CLIENT_SECRET`** in this setup.

## 9. GitHub Actions workflow

The workflow needs permission to request an OIDC token:

``` yaml
permissions:
  id-token: write
  contents: read
```

Example:

``` yaml
name: Deploy

on:
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: dev

    steps:
      - uses: actions/checkout@v4

      - name: Azure login
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Verify Azure context
        run: az account show -o table
```

`environment: dev` is significant. It causes GitHub's OIDC subject to
contain:

``` text
repo:YOUR_GITHUB_USER/YOUR_REPO:environment:dev
```

That must match the `subject` configured in the Entra federated
credential.

## 10. What happens during a deployment?

The authentication flow is roughly:

``` text
1. GitHub starts workflow
2. GitHub creates a short-lived signed OIDC token
3. Token says, among other things:
      issuer  = https://token.actions.githubusercontent.com
      subject = repo:...:environment:dev
4. azure/login sends that token to Microsoft Entra ID
5. Entra checks the App Registration's federated credential
6. If issuer + subject + audience match, Entra authenticates the
   workflow as the application's Service Principal
7. Azure RBAC determines what that Service Principal may do
8. Workflow can deploy within the allowed scope
```

There is no reusable Azure password stored in GitHub.

## 11. Authentication vs authorization

This distinction is important for Azure and AZ-104:

``` text
Federated credential / OIDC
        |
        v
AUTHENTICATION
"Who is this?"
        |
        |  Service Principal
        v
Azure RBAC
        |
        v
AUTHORIZATION
"What may it do?"
```

A valid OIDC login does not automatically grant access to Azure
resources. The service principal still needs an RBAC role assignment.

## 12. Common failure: "No subscriptions found"

If GitHub reports:

``` text
Attempting Azure CLI login by using OIDC...
Error: No subscriptions found for ...
```

check:

### Correct subscription and tenant

``` bash
az account show \
  --query '{subscriptionId:id, tenantId:tenantId}' \
  -o json
```

Compare these with GitHub's configured values.

### App Registration exists in this tenant

``` bash
az ad app list \
  --display-name "$APP_NAME" \
  --query '[].{name:displayName, clientId:appId, objectId:id}' \
  -o table
```

### Service Principal exists

``` bash
az ad sp show \
  --id "$CLIENT_ID" \
  --query '{name:displayName, clientId:appId, objectId:id}' \
  -o json
```

### Service Principal has RBAC access

``` bash
az role assignment list \
  --assignee-object-id "$SP_OBJECT_ID" \
  --all \
  -o table
```

### OIDC subject matches exactly

``` bash
az ad app federated-credential list \
  --id "$APP_OBJECT_ID" \
  -o table
```

For a GitHub Environment named `dev`, expect:

``` text
repo:YOUR_GITHUB_USER/YOUR_REPO:environment:dev
```

If GitHub says its subject is one value while Entra expects another,
authentication fails.

## 13. Safe to put this file in a public GitHub repository?

Yes, provided you keep actual credentials out of it.

Normally safe to expose:

``` text
Tenant ID
Subscription ID
Application/Client ID
Object IDs
resource-group names
App Registration names
Azure region
GitHub repository name
OIDC issuer
OIDC subject
```

These are identifiers/configuration, not proof of identity.

Do **not** commit:

``` text
client secrets
passwords
access tokens
refresh tokens
storage account keys
SAS tokens
private keys
connection strings containing credentials
GitHub personal access tokens
```

OIDC is useful specifically because this deployment does not require a
long-lived Azure client secret.

## 14. Cleanup

Delete the RBAC assignment/application when it is no longer needed.

To delete the App Registration:

``` bash
az ad app delete \
  --id "$APP_OBJECT_ID"
```

Deleting the application also makes the GitHub OIDC identity unusable.

Verify before deleting anything:

``` bash
az ad app show --id "$APP_OBJECT_ID"
az ad sp show --id "$CLIENT_ID"
```

## AZ-104 concepts exercised

This small setup connects several concepts that otherwise look unrelated
in the course:

``` text
Microsoft Entra ID
    App Registration
    Service Principal
    Federated identity

Azure RBAC
    Principal
    Role
    Scope
    Role assignment

Azure hierarchy
    Tenant
    Subscription
    Resource Group
    Resource

GitHub Actions
    OIDC workload identity
```

The central model to remember is:

``` text
IDENTITY                       PERMISSION

GitHub                         Resource Group
   |                                ^
   | OIDC                           |
   v                                | Contributor
App Registration                    |
   |                                |
   v                                |
Service Principal ------------------+
```

The App Registration/service principal answers **who the workload is**.\
The RBAC assignment answers **what that workload may do**.
