// ---------------------------------------------------------------------------
// Azure API Management — unified API façade for InsightPulse AI
// ---------------------------------------------------------------------------
// Sits behind Azure Front Door (ipai-fd-dev).
// All backend Container Apps are exposed exclusively through APIM path routes.
//
// Deploy:
//   az deployment group create \
//     --resource-group rg-ipai-dev \
//     --template-file infra/bicep/modules/apim.bicep \
//     --parameters apimName=apim-ipai-dev location=eastus2
// ---------------------------------------------------------------------------

@description('Name of the API Management instance')
param apimName string = 'apim-ipai-dev'

@description('Azure region')
param location string = resourceGroup().location

@description('Publisher email for APIM')
param publisherEmail string = 'platform@insightpulseai.com'

@description('Publisher name')
param publisherName string = 'InsightPulse AI'

@description('SKU: Developer for dev, Standard/Premium for prod')
@allowed(['Developer', 'Standard', 'Premium', 'Consumption'])
param skuName string = 'Developer'

@description('SKU capacity (ignored for Consumption)')
param skuCapacity int = 1

// ---------------------------------------------------------------------------
// Backend origins — Container App FQDNs
// ---------------------------------------------------------------------------
@description('Odoo web FQDN')
param odooBackendFqdn string = 'ipai-odoo-dev-web.internal.eastus2.azurecontainerapps.io'

@description('Auth service FQDN')
param authBackendFqdn string = 'ipai-auth-dev.internal.eastus2.azurecontainerapps.io'

@description('CRM service FQDN')
param crmBackendFqdn string = 'ipai-crm-dev.internal.eastus2.azurecontainerapps.io'

@description('MCP / agent service FQDN')
param mcpBackendFqdn string = 'ipai-mcp-dev.internal.eastus2.azurecontainerapps.io'

@description('OCR service FQDN')
param ocrBackendFqdn string = 'ipai-ocr-dev.internal.eastus2.azurecontainerapps.io'

// ---------------------------------------------------------------------------
// APIM Instance
// ---------------------------------------------------------------------------
resource apim 'Microsoft.ApiManagement/service@2023-09-01-preview' = {
  name: apimName
  location: location
  sku: {
    name: skuName
    capacity: skuCapacity
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    publisherEmail: publisherEmail
    publisherName: publisherName
    customProperties: {
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls11': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls10': 'false'
    }
  }
}

// ---------------------------------------------------------------------------
// Backends
// ---------------------------------------------------------------------------
var backends = [
  { name: 'odoo',  fqdn: odooBackendFqdn,  description: 'Odoo ERP' }
  { name: 'auth',  fqdn: authBackendFqdn,  description: 'Auth service' }
  { name: 'crm',   fqdn: crmBackendFqdn,   description: 'CRM service' }
  { name: 'mcp',   fqdn: mcpBackendFqdn,   description: 'MCP / Agent service' }
  { name: 'ocr',   fqdn: ocrBackendFqdn,   description: 'OCR service' }
]

resource apimBackends 'Microsoft.ApiManagement/service/backends@2023-09-01-preview' = [
  for backend in backends: {
    parent: apim
    name: 'backend-${backend.name}'
    properties: {
      url: 'https://${backend.fqdn}'
      protocol: 'http'
      description: backend.description
      tls: {
        validateCertificateChain: true
        validateCertificateName: true
      }
    }
  }
]

// ---------------------------------------------------------------------------
// Unified API  — api.insightpulseai.com
// ---------------------------------------------------------------------------
resource unifiedApi 'Microsoft.ApiManagement/service/apis@2023-09-01-preview' = {
  parent: apim
  name: 'ipai-unified-api'
  properties: {
    displayName: 'InsightPulse AI Unified API'
    path: 'api'
    protocols: ['https']
    subscriptionRequired: true
    subscriptionKeyParameterNames: {
      header: 'X-Api-Key'
      query: 'api-key'
    }
    serviceUrl: 'https://${odooBackendFqdn}'
    apiRevision: '1'
  }
}

// ---------------------------------------------------------------------------
// Operations — path-based routing
// ---------------------------------------------------------------------------

// /api/odoo/* → Odoo backend
resource opOdoo 'Microsoft.ApiManagement/service/apis/operations@2023-09-01-preview' = {
  parent: unifiedApi
  name: 'odoo-proxy'
  properties: {
    displayName: 'Odoo proxy'
    method: '*'
    urlTemplate: '/odoo/*'
    description: 'Proxy to Odoo ERP backend'
  }
}

resource policyOdoo 'Microsoft.ApiManagement/service/apis/operations/policies@2023-09-01-preview' = {
  parent: opOdoo
  name: 'policy'
  properties: {
    value: '''
<policies>
  <inbound>
    <base />
    <set-backend-service backend-id="backend-odoo" />
    <rewrite-uri template="/{remaining}" />
    <set-header name="X-Forwarded-Prefix" exists-action="override">
      <value>/api/odoo</value>
    </set-header>
  </inbound>
  <backend><base /></backend>
  <outbound><base /></outbound>
  <on-error><base /></on-error>
</policies>
'''
    format: 'xml'
  }
}

// /api/auth/* → Auth backend
resource opAuth 'Microsoft.ApiManagement/service/apis/operations@2023-09-01-preview' = {
  parent: unifiedApi
  name: 'auth-proxy'
  properties: {
    displayName: 'Auth proxy'
    method: '*'
    urlTemplate: '/auth/*'
    description: 'Proxy to Auth service'
  }
}

resource policyAuth 'Microsoft.ApiManagement/service/apis/operations/policies@2023-09-01-preview' = {
  parent: opAuth
  name: 'policy'
  properties: {
    value: '''
<policies>
  <inbound>
    <base />
    <set-backend-service backend-id="backend-auth" />
    <rewrite-uri template="/{remaining}" />
    <set-header name="X-Forwarded-Prefix" exists-action="override">
      <value>/api/auth</value>
    </set-header>
  </inbound>
  <backend><base /></backend>
  <outbound><base /></outbound>
  <on-error><base /></on-error>
</policies>
'''
    format: 'xml'
  }
}

// /api/crm/* → CRM backend
resource opCrm 'Microsoft.ApiManagement/service/apis/operations@2023-09-01-preview' = {
  parent: unifiedApi
  name: 'crm-proxy'
  properties: {
    displayName: 'CRM proxy'
    method: '*'
    urlTemplate: '/crm/*'
    description: 'Proxy to CRM service'
  }
}

resource policyCrm 'Microsoft.ApiManagement/service/apis/operations/policies@2023-09-01-preview' = {
  parent: opCrm
  name: 'policy'
  properties: {
    value: '''
<policies>
  <inbound>
    <base />
    <set-backend-service backend-id="backend-crm" />
    <rewrite-uri template="/{remaining}" />
    <set-header name="X-Forwarded-Prefix" exists-action="override">
      <value>/api/crm</value>
    </set-header>
  </inbound>
  <backend><base /></backend>
  <outbound><base /></outbound>
  <on-error><base /></on-error>
</policies>
'''
    format: 'xml'
  }
}

// /api/agents/* → MCP backend
resource opAgents 'Microsoft.ApiManagement/service/apis/operations@2023-09-01-preview' = {
  parent: unifiedApi
  name: 'agents-proxy'
  properties: {
    displayName: 'Agents proxy'
    method: '*'
    urlTemplate: '/agents/*'
    description: 'Proxy to MCP / Agent service'
  }
}

resource policyAgents 'Microsoft.ApiManagement/service/apis/operations/policies@2023-09-01-preview' = {
  parent: opAgents
  name: 'policy'
  properties: {
    value: '''
<policies>
  <inbound>
    <base />
    <set-backend-service backend-id="backend-mcp" />
    <rewrite-uri template="/{remaining}" />
    <set-header name="X-Forwarded-Prefix" exists-action="override">
      <value>/api/agents</value>
    </set-header>
  </inbound>
  <backend><base /></backend>
  <outbound><base /></outbound>
  <on-error><base /></on-error>
</policies>
'''
    format: 'xml'
  }
}

// /api/ocr/* → OCR backend
resource opOcr 'Microsoft.ApiManagement/service/apis/operations@2023-09-01-preview' = {
  parent: unifiedApi
  name: 'ocr-proxy'
  properties: {
    displayName: 'OCR proxy'
    method: '*'
    urlTemplate: '/ocr/*'
    description: 'Proxy to OCR service'
  }
}

resource policyOcr 'Microsoft.ApiManagement/service/apis/operations/policies@2023-09-01-preview' = {
  parent: opOcr
  name: 'policy'
  properties: {
    value: '''
<policies>
  <inbound>
    <base />
    <set-backend-service backend-id="backend-ocr" />
    <rewrite-uri template="/{remaining}" />
    <set-header name="X-Forwarded-Prefix" exists-action="override">
      <value>/api/ocr</value>
    </set-header>
  </inbound>
  <backend><base /></backend>
  <outbound><base /></outbound>
  <on-error><base /></on-error>
</policies>
'''
    format: 'xml'
  }
}

// ---------------------------------------------------------------------------
// Global policy — rate limiting, CORS, diagnostics
// ---------------------------------------------------------------------------
resource globalPolicy 'Microsoft.ApiManagement/service/policies@2023-09-01-preview' = {
  parent: apim
  name: 'policy'
  properties: {
    value: '''
<policies>
  <inbound>
    <cors allow-credentials="true">
      <allowed-origins>
        <origin>https://erp.insightpulseai.com</origin>
        <origin>https://www.insightpulseai.com</origin>
        <origin>https://api.insightpulseai.com</origin>
      </allowed-origins>
      <allowed-methods preflight-result-max-age="300">
        <method>GET</method>
        <method>POST</method>
        <method>PUT</method>
        <method>PATCH</method>
        <method>DELETE</method>
        <method>OPTIONS</method>
      </allowed-methods>
      <allowed-headers>
        <header>*</header>
      </allowed-headers>
    </cors>
    <rate-limit calls="100" renewal-period="60" />
  </inbound>
  <backend><base /></backend>
  <outbound>
    <set-header name="X-Powered-By" exists-action="delete" />
    <set-header name="Server" exists-action="delete" />
  </outbound>
  <on-error><base /></on-error>
</policies>
'''
    format: 'xml'
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------
output apimId string = apim.id
output apimGatewayUrl string = apim.properties.gatewayUrl
output apimManagedIdentityPrincipalId string = apim.identity.principalId
