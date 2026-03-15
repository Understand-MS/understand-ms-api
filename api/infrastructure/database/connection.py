from azure.cosmos.aio import CosmosClient
from azure.identity.aio import DefaultAzureCredential

from api.core.config import settings


def get_cosmos_client() -> CosmosClient:
    credential = DefaultAzureCredential()
    return CosmosClient(url=settings.cosmos_url, credential=credential)