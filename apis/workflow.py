from typing import Literal

from fastapi import APIRouter, Query
from services import workflow_service

from configuration import keyvault

workflow_router = APIRouter(prefix="/api/workflow/v1", tags=["Workflow apis"])

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


@workflow_router.get("/workflow")
def get_workflows(env: Literal[*env_list] = Query(...),
                  data_partition: Literal[*data_partition_list] = Query(...)):
    return workflow_service.get_workflows(env, data_partition)


@workflow_router.get("/workflow/{workflow_name}")
def get_workflow(env: Literal[*env_list] = Query(...),
                 dag: Literal[*dag_list] = Query(...),
                 data_partition: Literal[*data_partition_list] = Query(...)):
    return workflow_service.get_workflow(env, dag, data_partition)


@workflow_router.post("/workflow")
def register_workflow(env: Literal[*env_list] = Query(...),
                      dag: Literal[*dag_list] = Query(...)):
    return workflow_service.register_workflow(env, dag)


@workflow_router.post("/trigger_workflow")
def trigger_workflow(env: Literal[*env_list] = Query(...),
                     data_partition: Literal[*data_partition_list] = Query(...),
                     dag: Literal[*dag_list] = Query(...),
                     file_id: str = "tknxchange:dataset--File.Generic:04ca232a-554c-4d90-962a-d296506d6ba8"):
    return workflow_service.trigger_workflow(env, data_partition, dag, file_id)
