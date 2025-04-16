from typing import Literal

from fastapi import APIRouter, Query

from configuration import keyvault
from models.data_models import StatusPayload, StatusQuery
from services import status_service

status_router = APIRouter(tags=["Status publish and Retreive"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]

data_partition_list = set()
for key in keyvault.keys():
    if isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") not in [None,""]:
        data_partition_list.add(*keyvault.get(key).get("data_partitions"))


@status_router.post("/api/status-publisher/v1/status")
def publish_status(status: StatusPayload,
                   env: Literal[*env_list] = Query(...),
                   data_partition: Literal[*data_partition_list] = Query(...),
                   ):
    return status_service.publish_status(env, data_partition, status)


@status_router.post("/api/status-processor/v1/status/query")
def get_status(status_filter: StatusQuery,
               env: Literal[*env_list] = Query(...),
               data_partition: Literal[*data_partition_list] = Query(...),
               ):
    return status_service.get_status(env, data_partition, status_filter)
