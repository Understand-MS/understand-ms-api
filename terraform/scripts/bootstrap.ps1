# Optional to create resource group and storage account for the Terraform state
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

Write-Host "Checking if Storage Account exists..."
$saCheck = az storage account check-name --name $StorageAccount | ConvertFrom-Json

if ($saCheck.nameAvailable) {
    Write-Host "Creating Storage Account..."
    az storage account create `
        --name $StorageAccount `
        --resource-group $ResourceGroup `
        --location $Location `
        --sku Standard_LRS `
        --kind StorageV2 `
        --output none
} else {
    Write-Host "Storage account already exists."
}

Write-Host "Getting Storage Account Key..."
$storageKey = az storage account keys list `
    --resource-group $ResourceGroup `
    --account-name $StorageAccount `
    --query "[0].value" -o tsv

Write-Host "Creating Blob Container if not exists..."
try {
    az storage container create `
        --name $ContainerName `
        --account-name $StorageAccount `
        --account-key $storageKey `
        --output none
} catch {
    Write-Host "Blob container '$ContainerName' already exists."
}

Write-Host "Bootstrap completed successfully."