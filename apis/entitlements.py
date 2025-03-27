from fastapi import APIRouter, Query
from services import entitlements_service

from configuration import keyvault

ent_router = APIRouter(prefix="/api/entitlements/v2", tags=["entitlement apis"])


@ent_router.get("/groups")
def get_groups(env: str = Query(None, description="Environment",
                                enum=keyvault["envs-ltops"] + keyvault["envs"])):
    return entitlements_service.get_groups(env)


@ent_router.get("/members/{user}/groups",
                description="data.default.owners@domain, pgorade@slb.com, users.datalake.admins@domain")
def get_members_groups(user: str = "user.datalake.admins@domain",
                       env: str = Query(None, description="Environment",
                                        enum=keyvault["envs-ltops"] + keyvault["envs"]),
                       member_type: str = Query("DATA", enum=["USER", "DATA", "SERVICE"])
                       ):
    return entitlements_service.get_members_groups(user, env, member_type)
