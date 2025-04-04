from fastapi import APIRouter, Query

from configuration import keyvault
from models.data_models import resource_value
from services import data_partition_registry

data_partition_router = APIRouter(prefix="/ccm/dataPartitionRegistry/v2", tags=["data partition registry apis"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]

data_partition_list = list({keyvault[key].get("data_partition_id") for key in keyvault.keys() if
                            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None})


@data_partition_router.get("/dataPartitions/{dataPartitionId}/applications/{appCode}/resources")
def get_resources(region: str = Query(default="us", enum=["au", "us"]),
                  env: str = Query(None, description="Environment",
                                   enum=env_list),
                  data_partition: str = Query(None, description="data-partition",
                                              enum=data_partition_list),
                  app_code: str = Query(default="workflowservices")
                  ):
    return data_partition_registry.fetch_resources(region, env, data_partition=data_partition, app_code=app_code)


@data_partition_router.get("/dataPartitions/{dataPartitionId}/applications/{appCode}/resources/{resource_key}")
def get_resource(region: str = Query(default="us", enum=["au", "us"]),
                 env: str = Query(None, description="Environment",
                                  enum=env_list),
                 data_partition: str = Query(None, description="data-partition",
                                             enum=data_partition_list),
                 app_code: str = Query(default="workflowservices"),
                 resource_key: str = "IP_URL"
                 ):
    return data_partition_registry.fetch_resource(region, env, data_partition=data_partition, app_code=app_code,
                                                  resource_key=resource_key)


@data_partition_router.put("/dataPartitions/{dataPartitionId}/applications/{appCode}/resources/{resourceKey}")
def put_resource(resource: resource_value,
                 region: str = Query(default="us", enum=["au", "us"]),
                 env: str = Query(None, description="Environment",
                                  enum=env_list),
                 data_partition: str = Query(None, description="data-partition",
                                             enum=data_partition_list),
                 app_code: str = Query(default="workflowservices"),
                 resource_key: str = "IP_URL",
                 ):
    return data_partition_registry.create_resource(region, resource, env, data_partition=data_partition,
                                                   app_code=app_code,
                                                   resource_key=resource_key)
