from typing import Literal

from fastapi import APIRouter, Query
from services import entitlements_service

from configuration import keyvault

ent_router = APIRouter(prefix="/api/entitlements/v2", tags=["Entitlement apis"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]

data_partition_list = set()
for key in keyvault.keys():
    if isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") not in [None, ""]:
        data_partition_list.update(keyvault.get(key).get("data_partitions"))


@ent_router.get("/groups")
def get_groups(env: Literal[*env_list] = Query(...),
               data_partition: Literal[*data_partition_list] = Query(...)):
    return entitlements_service.get_groups(env, data_partition)


@ent_router.get("/compare_groups")
def compare_groups(env_first: Literal[*env_list] = Query(...),
                   data_partition_first: Literal[*data_partition_list] = Query(...),
                   env_second: Literal[*env_list] = Query(...),
                   data_partition_second: Literal[*data_partition_list] = Query(...),
                   base_first: bool = True
                   ):
    return entitlements_service.compare_groups(env_first, data_partition_first, env_second, data_partition_second, base_first)


@ent_router.get("/members/{user}/groups",
                description="data.default.owners@domain, pgorade@slb.com, "
                            "users.datalake.editors@arm-perf.dataservices.energy")
def get_members_groups(user: str = "user.datalake.admins@domain",
                       env: Literal[*env_list] = Query(...),
                       data_partition: Literal[*data_partition_list] = Query(...),
                       member_type: str = Query("DATA", enum=["USER", "DATA", "SERVICE"])
                       ):
    return entitlements_service.get_members_groups(user, env, data_partition, member_type)
