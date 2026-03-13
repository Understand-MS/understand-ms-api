# scripts/bootstrap.ps1
param(
    [string]$ResourceGroup = "understand-ms-rg",
    [string]$Location = "northeurope",
    [string]$StorageAccount = "understandmstfstateaccount",
    [string]$ContainerName = "tfstate"
)

Write-Host "Checking or creating Resource Group..."
az group create `
    --name $ResourceGroup `
    --location $Location `
    --output none
Write-Host "Resource Group ensured."

Write-Host "Checking if Storage Account exists in Resource Group..."
try {
    $sa = az storage account show `
        --name $StorageAccount `
        --resource-group $ResourceGroup `
        --output json 2>$null | ConvertFrom-Json
} catch {
    $sa = $null
}

if (-not $sa) {
    Write-Host "Storage Account does not exist. Creating..."
    az storage account create `
        --name $StorageAccount `
        --resource-group $ResourceGroup `
        --location $Location `
        --sku Standard_LRS `
        --kind StorageV2 `
        --output none
    Write-Host "Storage Account created."
} else {
    Write-Host "Storage Account already exists."
}

Write-Host "Retrieving Storage Account key..."
$storageKey = az storage account keys list `
    --resource-group $ResourceGroup `
    --account-name $StorageAccount `
    --query "[0].value" -o tsv

if (-not $storageKey) {
    throw "Failed to retrieve Storage Account key. Exiting."
}

Write-Host "Creating Blob Container if not exists..."
try {
    az storage container create `
        --name $ContainerName `
        --account-name $StorageAccount `
        --account-key $storageKey `
        --output none
    Write-Host "Blob container ensured."
} catch {
    Write-Host "Blob container '$ContainerName' already exists or failed to create."
}