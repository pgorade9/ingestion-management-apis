from typing import Literal

from fastapi import APIRouter, Query

from configuration import keyvault
from services import user_association_service

user_association_router = APIRouter(prefix="/ccm/dataPartitionRegistry/v2", tags=["Data Partition Registry apis"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]


@user_association_router.get("/dataPartitions/{dataPartitionId}/applications/{appCode}/resources")
def get_resources(region: Literal["eu", "us"] = Query(...),
                  env: Literal[*env_list] = Query(...),
                  billing_account_id: str = Query(default="DIGITAL2020"),
                  contract_id: str = Query(default="2T6DR4TH1T"),
                  app_code: str = Query(default="datamanager")
                  ):
    return user_association_service.get_role_assignments(region, env, billing_account_id, contract_id, app_code)
