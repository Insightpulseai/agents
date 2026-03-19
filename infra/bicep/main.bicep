// ---------------------------------------------------------------------------
// InsightPulse AI — main Bicep orchestration
// ---------------------------------------------------------------------------
// Usage:
//   az deployment group create \
//     --resource-group rg-ipai-dev \
//     --template-file infra/bicep/main.bicep \
//     --parameters environment=dev
// ---------------------------------------------------------------------------

targetScope = 'resourceGroup'

@allowed(['dev', 'staging', 'prod'])
param environment string = 'dev'

@description('Azure region')
param location string = resourceGroup().location

// ---------------------------------------------------------------------------
// API Management
// ---------------------------------------------------------------------------
module apim 'modules/apim.bicep' = {
  name: 'apim-deployment'
  params: {
    apimName: 'apim-ipai-${environment}'
    location: location
    skuName: environment == 'prod' ? 'Standard' : 'Developer'
    skuCapacity: environment == 'prod' ? 2 : 1
  }
}

output apimGatewayUrl string = apim.outputs.apimGatewayUrl
output apimManagedIdentityPrincipalId string = apim.outputs.apimManagedIdentityPrincipalId
