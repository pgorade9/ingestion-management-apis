from typing import Literal

from fastapi import APIRouter, Query

from configuration import keyvault
from services import token_exchange_service

token_exchange_router = APIRouter(prefix="/api/workflow/v1/token_exchange", tags=["Token Exchange apis"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]

data_partition_list = list({keyvault[key].get("data_partition_id") for key in keyvault.keys() if
                            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None})


@token_exchange_router.get("/workflow/getSession")
def get_session(env: Literal[*env_list] = Query(...),
                data_partition_id: Literal[*data_partition_list] = Query(...),
                user_id: str = ""):
    return token_exchange_service.get_session(env, data_partition_id, user_id)


@token_exchange_router.get("/workflow/get_endpoint_id")
def get_endpoint_id(env: Literal[*env_list] = Query(...),
                    data_partition_id: Literal[*data_partition_list] = Query(...),
                    ):
    return token_exchange_service.get_endpoint_id(env, data_partition_id)


@token_exchange_router.get("/workflow/get_resource_id")
def get_resource_id(env: Literal[*env_list] = Query(...),
                    endpoint_id: str="",
                    ):
    return token_exchange_service.get_resource_id(env, endpoint_id)


@token_exchange_router.get("/workflow/get_exchange_token")
def get_exchange_token(env: Literal[*env_list] = Query(...),
                    resource_id: str="",
                    ):
    return token_exchange_service.exchange_token(env, resource_id)