from typing import Literal

from fastapi import APIRouter, Query
from services import legal_tag_service

from configuration import keyvault

legal_router = APIRouter(prefix="/api/legal/v1", tags=["Legal tag apis"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]

@legal_router.get("/legaltags")
def get_groups(env: Literal[*env_list] = Query(...)):
    return legal_tag_service.get_legal_tags(env)
