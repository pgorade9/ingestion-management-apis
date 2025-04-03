from fastapi import APIRouter, Query
from services import data_partition_registry

from configuration import keyvault

data_partition_router = APIRouter(prefix="/ccm/dataPartitionRegistry/v2", tags=["data partition registry apis"])


@data_partition_router.get("/dataPartitions/{dataPartitionId}/applications/{appCode}/resources")
def get_resources(region: str = Query(default="us", enum=["au", "us"]),
                  env: str = Query(None, description="Environment",
                                   enum=keyvault["envs-ltops"] + keyvault["envs"]),
                  data_partition: str = Query(None, description="data-partition",
                                              enum=[keyvault[e]["data_partition_id"] for e in keyvault["envs-ltops"]]),
                  app_code: str = Query("workflowservices")
                  ):
    return data_partition_registry.fetch_resources(region, env, data_partition=data_partition, app_code=app_code)


@data_partition_router.get("/dataPartitions/{dataPartitionId}/applications/{appCode}/resources/{resource_key}")
def get_resource(region: str = Query(default="us", enum=["au", "us"]),
                 env: str = Query(None, description="Environment",
                                  enum=keyvault["envs-ltops"] + keyvault["envs"]),
                 data_partition: str = Query(None, description="data-partition",
                                             enum=[keyvault[e]["data_partition_id"] for e in keyvault["envs-ltops"]]),
                 app_code: str = Query("workflowservices"),
                 resource_key: str = "IP_URL"
                 ):
    return data_partition_registry.fetch_resource(region, env, data_partition=data_partition, app_code=app_code,
                                                  resource_key=resource_key)

