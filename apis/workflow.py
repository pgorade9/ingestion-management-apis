from typing import Literal

from fastapi import APIRouter, Query
from services import workflow_service

from configuration import keyvault

workflow_router = APIRouter(prefix="/api/workflow/v1", tags=["workflow apis"])

env_list = [key for key in keyvault.keys() if
            isinstance(keyvault[key], dict) and keyvault[key].get("data_partition_id") is not None]


@workflow_router.get("/workflow")
def get_workflows(env: Literal[*env_list] = Query(...)):
    return workflow_service.get_workflows(env)


@workflow_router.get("/workflow/{workflow_name}")
def get_workflow(env: Literal[*env_list] = Query(...),
                 dag: str = Query(None, enum=["csv_parser_wf_status_gsm",
                                              "wellbore_ingestion_wf_gsm",
                                              "doc_ingestor_azure_ocr_wf",
                                              "shapefile_ingestor_wf_status_gsm",
                                              "Osdu_ingest"], description="workflow_name")):
    return workflow_service.get_workflow(env, dag)


@workflow_router.post("/workflow}")
def register_workflow(env: Literal[*env_list] = Query(...),
                      dag: str = Query(None, enum=["csv_parser_wf_status_gsm",
                                                   "wellbore_ingestion_wf_gsm",
                                                   "doc_ingestor_azure_ocr_wf",
                                                   "shapefile_ingestor_wf_status_gsm",
                                                   "Osdu_ingest"], description="workflow_name")):
    return workflow_service.register_workflow(env, dag)
