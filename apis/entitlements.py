from typing import Literal

from fastapi import APIRouter, Query
from services import entitlements_service

from configuration import keyvault

ent_router = APIRouter(prefix="/api/entitlements/v2", tags=["entitlement apis"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]


@ent_router.get("/groups")
def get_groups(env: Literal[*env_list] = Query(...)):
    return entitlements_service.get_groups(env)


@ent_router.get("/members/{user}/groups",
                description="data.default.owners@domain, pgorade@slb.com, users.datalake.admins@domain")
def get_members_groups(user: str = "user.datalake.admins@domain",
                       env: Literal[*env_list] = Query(...),
                       member_type: str = Query("DATA", enum=["USER", "DATA", "SERVICE"])
                       ):
    return entitlements_service.get_members_groups(user, env, member_type)
