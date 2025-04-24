from typing import Literal

from fastapi import APIRouter, Query

from models.data_models import SearchQuery
from services import workflow_service, search_service

from configuration import keyvault

search_router = APIRouter(prefix="/api/search/v1", tags=["Search apis"])

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


@search_router.post("/search")
def get_workflows(
        search_query: SearchQuery,
        env: Literal[*env_list] = Query(...),
        data_partition: Literal[*data_partition_list] = Query(...)):
    return search_service.search_entire_kind(env, data_partition, search_query)
