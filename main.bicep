

// Parameters
// @description('Name of the environment')
// param environment string

@description('Optional. Location for all resources.')
param location string = resourceGroup().location

// @description('resource group name')
// param resource_group_name string

param storageAccountSku string = 'Standard_LRS'

@description('The storage account name')
param storageAccountName string = uniqueString(resourceGroup().id)

@description('Optional. Dynamically tags from JSON file')
param tags object = {}



resource stg 'Microsoft.Storage/storageAccounts@2022-09-01'={
  kind:'BlobStorage'
  location:location
  name:storageAccountName
  //scope: resourceGroup(resource_group_name)
  sku: {
    name: storageAccountSku
  }
  tags:tags
}
