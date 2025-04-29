from typing import Literal

from fastapi import APIRouter, Query

from configuration import keyvault
from models.data_models import CreateSubscriptionPayload
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


@register_router.post("/subscription")
def create_subscription(env: Literal[*env_list] = Query(...),
                        data_partition: Literal[*data_partition_list] = Query(...),
                        topic_name: Literal["statuschangedtopic", "recordstopic", "schemachangedtopic"] = Query(...),
                        push_endpoint_domain: Literal["osdu", "lightops"] = Query(...),
                        hmac_key: str = "17062990c29797c20004f224b93cec"):
    return register_service.create_subscription(env, data_partition, topic_name, push_endpoint_domain, hmac_key)


@register_router.get("/subscription/{id}")
def get_subscription(env: Literal[*env_list] = Query(...),
                     data_partition: Literal[*data_partition_list] = Query(...),
                     topic_name: Literal["statuschangedtopic", "recordstopic", "schemachangedtopic"] = Query(...),
                     push_endpoint_domain: Literal["osdu", "lightops"] = Query(...)):
    return register_service.get_subscription(env, data_partition, topic_name, push_endpoint_domain)


@register_router.delete("/subscription/{id}")
def delete_subscription(env: Literal[*env_list] = Query(...),
                        data_partition: Literal[*data_partition_list] = Query(...),
                        topic_name: Literal["statuschangedtopic", "recordstopic", "schemachangedtopic"] = Query(...),
                        push_endpoint_domain: Literal["osdu", "lightops"] = Query(...)):
    return register_service.delete_subscription(env, data_partition, topic_name, push_endpoint_domain)
