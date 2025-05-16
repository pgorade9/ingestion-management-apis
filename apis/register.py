from typing import Literal

from fastapi import APIRouter, Query

from configuration import keyvault
from models.data_models import HMACSecret
from services import register_service

register_router = APIRouter(prefix="/api/register/v1", tags=["Register apis"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]

dag_list = ["csv_parser_wf_status_gsm",
            "wellbore_ingestion_wf_gsm",
            "doc_ingestor_azure_ocr_wf",
            "shapefile_ingestor_wf_status_gsm",
            "Osdu_ingest",
            "segy_indexer_wf_gsm",
            "segy_metadata_ingestor_wf_gsm",
            "segy_to_vds_conversion_wf_gsm",
            "segy_to_zgy_conversion_wf_gsm",
            "zgy_indexer_wf_gsm",
            "zgy_metadata_ingestor_wf_gsm"]

data_partition_list = set()
for key in keyvault.keys():
    if isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") not in [None, ""]:
        data_partition_list.update(keyvault.get(key).get("data_partitions"))

topic_list = ["statuschangedtopic", "recordstopic", "schemachangedtopic"]

listener_service_list = ["notification-listener", "listener-service"]


@register_router.post("/subscription_with_push_endpoint")
def create_subscription_with_push_endpoint(env: Literal[*env_list] = Query(...),
                                           data_partition: Literal[*data_partition_list] = Query(...),
                                           subscription_domain: Literal["osdu", "lightops"] = Query(...),
                                           push_endpoint: str = Query(default="https://evt-dw.app.evt-1.lightops.slb"
                                                                              ".com/dm/notification-listener/events"
                                                                              "/v1/statusTopic/mpdf-large-sandbox-eu",
                                                                      description="required"),
                                           topic_name: Literal[*topic_list] = Query(...),
                                           hmac_key: str = "5da75ef1e14df685672db02ea26a82"):
    return register_service.create_subscription_with_push_endpoint(env, data_partition, subscription_domain,
                                                                   push_endpoint, topic_name, hmac_key)


@register_router.post("/subscription")
def create_subscription(env: Literal[*env_list] = Query(...),
                        data_partition: Literal[*data_partition_list] = Query(...),
                        subscription_domain: Literal["osdu", "lightops"] = Query(...),
                        listener_service_name: Literal[*listener_service_list] = Query(...),
                        topic_name: Literal[*topic_list] = Query(...),
                        push_endpoint_namespace: Literal["sdfs", "dw"] = Query(default="dw"),

                        hmac_key: str = "5da75ef1e14df685672db02ea26a82"):
    return register_service.create_subscription(env, data_partition, subscription_domain, listener_service_name,
                                                topic_name, push_endpoint_namespace, hmac_key)


@register_router.get("/subscription/{id}")
def get_subscription(env: Literal[*env_list] = Query(...),
                     data_partition: Literal[*data_partition_list] = Query(...),
                     subscription_domain: Literal["osdu", "lightops"] = Query(...),
                     listener_service_name: Literal[*listener_service_list] = Query(...),
                     topic_name: Literal[*topic_list] = Query(...),
                     push_endpoint_namespace: Literal["sdfs", "dw"] = Query(default="dw")):
    return register_service.get_subscription(env, data_partition, subscription_domain, listener_service_name,
                                             topic_name, push_endpoint_namespace)


@register_router.get("/subscription", description="Displays the HMAC secret value")
def get_subscription_from_notification_id(env: Literal[*env_list] = Query(...),
                                          data_partition: Literal[*data_partition_list] = Query(...),
                                          notification_id: str = Query("de-30b404f1-4f12-4ece-b6bf-0bef800804dd",
                                                                       description="Use mpdf-large-sandbox-eu with EVT")):
    return register_service.get_subscription_notification_id(env, data_partition, notification_id)


@register_router.delete("/subscription/{id}")
def delete_subscription(env: Literal[*env_list] = Query(...),
                        data_partition: Literal[*data_partition_list] = Query(...),
                        listener_service_name: Literal[*listener_service_list] = Query(...),
                        topic_name: Literal[*topic_list] = Query(...),
                        push_endpoint_namespace: Literal["sdfs", "dw"] = Query(...)):
    return register_service.delete_subscription(env, data_partition, listener_service_name, topic_name,
                                                push_endpoint_namespace)


@register_router.put("/subscription/{id}")
def upddate_hmac(hmac_secret: HMACSecret, env: Literal[*env_list] = Query(...),
                 data_partition: Literal[*data_partition_list] = Query(...),
                 subscription_domain: Literal["osdu", "lightops"] = Query(...),
                 listener_service_name: Literal[*listener_service_list] = Query(...),
                 topic_name: Literal[*topic_list] = Query(...),
                 push_endpoint_namespace: Literal["sdfs", "dw"] = Query(...)):
    return register_service.update_secret(hmac_secret, env, data_partition, subscription_domain, listener_service_name,
                                          topic_name,
                                          push_endpoint_namespace)


@register_router.get("/push_endpoint", description="Ping Push Endpoint")
def validate_push_endpoint(env: Literal[*env_list] = Query(...),
                           data_partition: Literal[*data_partition_list] = Query(...),
                           push_endpoint: str = Query("https://evt-dw.app.evt-1.lightops.slb.com/dm/notification"
                                                      "-listener/events/v1/statusTopic/mpdf-large-sandbox-eu",
                                                      description="Use mpdf-large-sandbox-eu with EVT"),
                           crc: str = Query("test"),
                           hmac: str = Query("5da75ef1e14df685672db02ea26a82")
                           ):
    return register_service.validate_push_endpoint(env, data_partition, push_endpoint, crc, hmac)
