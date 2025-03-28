from fastapi import APIRouter, Query
from services import legal_tag_service

from configuration import keyvault

legal_router = APIRouter(prefix="/api/legal/v1", tags=["legal tag apis"])


@legal_router.get("/legaltags")
def get_groups(env: str = Query(None, description="Environment",
                                enum=keyvault["envs-ltops"] + keyvault["envs"])):
    return legal_tag_service.get_legal_tags(env)
