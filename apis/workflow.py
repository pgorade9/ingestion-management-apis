from fastapi import APIRouter, Query
from services import workflow_service

from configuration import keyvault

workflow_router = APIRouter(prefix="/api/workflow/v1", tags=["workflow apis"])


@workflow_router.get("/workflow")
def get_workflows(env: str = Query(None, description="Environment",
                                   enum=keyvault["envs-ltops"] + keyvault["envs"])):
    return workflow_service.get_workflows(env)


@workflow_router.get("/workflow/{workflow_name}")
def get_workflow(env: str = Query(None, description="Environment",
                                  enum=keyvault["envs-ltops"] + keyvault["envs"]),
                 dag: str = Query(None, enum=["csv_parser_wf_status_gsm",
                                              "wellbore_ingestion_wf_gsm",
                                              "doc_ingestor_azure_ocr_wf",
                                              "shapefile_ingestor_wf_status_gsm",
                                              "Osdu_ingest"], description="workflow_name")):
    return workflow_service.get_workflow(env, dag)
