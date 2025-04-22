from typing import Literal

from fastapi import APIRouter, Query

from configuration import keyvault
from models.data_models import ResourceValue
from services import data_partition_registry

data_partition_router = APIRouter(prefix="/ccm/dataPartitionRegistry/v2", tags=["Data Partition Registry apis"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]

data_partition_list = set()
for key in keyvault.keys():
    if isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") not in [None,""]:
        data_partition_list.update(keyvault.get(key).get("data_partitions"))

@data_partition_router.get("/dataPartitions/{dataPartitionId}/applications/{appCode}/resources")
def get_resources(region: Literal["eu", "us"] = Query(...),
                  env: Literal[*env_list] = Query(...),
                  data_partition: Literal[*data_partition_list] = Query(...),
                  app_code: str = Query(default="workflowservices")
                  ):
    return data_partition_registry.fetch_resources(region, env, data_partition=data_partition, app_code=app_code)


@data_partition_router.get("/dataPartitions/{dataPartitionId}/applications/{appCode}/resources/{resource_key}")
def get_resource(region: Literal["eu", "us"] = Query(...),
                 env: Literal[*env_list] = Query(...),
                 data_partition: Literal[*data_partition_list] = Query(...),
                 app_code: str = Query(default="workflowservices"),
                 resource_key: str = "IP_URL"
                 ):
    return data_partition_registry.fetch_resource(region, env, data_partition=data_partition, app_code=app_code,
                                                  resource_key=resource_key)


@data_partition_router.put("/dataPartitions/{dataPartitionId}/applications/{appCode}/resources/{resourceKey}")
def put_resource(resource: ResourceValue,
                 region: Literal["eu", "us"] = Query(...),
                 env: Literal[*env_list] = Query(...),
                 data_partition: Literal[*data_partition_list] = Query(...),
                 app_code: str = Query(default="workflowservices"),
                 resource_key: str = "IP_URL",
                 ):
    return data_partition_registry.create_resource(resource, region, env, data_partition=data_partition,
                                                   app_code=app_code,
                                                   resource_key=resource_key)


if __name__=="__main__":
    data_partition_list = set()
    for key in keyvault.keys():
        if isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") not in [None,""]:
            data_partition_list.update(keyvault.get(key).get("data_partitions"))
    print(f"{data_partition_list=}")
