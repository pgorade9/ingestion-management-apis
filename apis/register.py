from typing import Literal

from fastapi import APIRouter, Query

from models.data_models import CreateSubscriptionPayload
from services import workflow_service, register_service

from configuration import keyvault

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


@register_router.post("/subscription")
def create_subscription(payload: CreateSubscriptionPayload,
                        env: Literal[*env_list] = Query(...),
                        data_partition: Literal[*data_partition_list] = Query(...)):
    return register_service.create_subscription(env, data_partition, payload)


@register_router.delete("/subscription/{id}")
def delete_subscription(env: Literal[*env_list] = Query(...),
                        data_partition: Literal[*data_partition_list] = Query(...),
                        topic_name: str = "statuschangedtopic",
                        push_endpoint: str = "https://dataworkflowservices-evd-sdfs.app.evd-2.lightops.slb.com/api/listener-service/partition/admedev01-dp2/topic/statuschangedtopic"):
    return register_service.delete_subscription(env, data_partition, topic_name, push_endpoint)
