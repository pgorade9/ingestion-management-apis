import json

import requests

from configuration import keyvault
from utils.token_utils import get_token


def get_workflows(env, data_partition):
    url = f"{keyvault[env]['seds_dns_host']}/api/workflow/v1/workflow"
    payload = ""
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        # print(f"{response_json=}")
        return response_json
    else:
        msg = f"Error occurred while fetching workflows {url=}. {response.text}"
        return {"msg": msg}


def get_workflow(env, dag, data_partition):
    url = f"{keyvault[env]['seds_dns_host']}/api/workflow/v1/workflow/{dag}"
    payload = ""
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        # print(f"{response_json=}")
        return response_json
    else:
        msg = f"Error occurred while fetching workflows {url=}. {response.text}"
        return {"msg": msg}


def register_workflow(env, dag):
    url = f"{keyvault[env]['seds_dns_host']}/api/workflow/v1/workflow"
    desc = {
        "shapefile_ingestor_wf_status_gsm": "Shapefile Ingestion",
        "csv_parser_wf_status_gsm": "CSV Parser",
        "wellbore_ingestion_wf_gsm": "Wellbore Ingestion",
        "doc_ingestor_azure_ocr_wf": "Document Ingestion"
    }
    payload = {
        "description": f"{dag if desc.get(dag) is None else desc.get(dag)}",
        "registrationInstructions": {
            "dagContent": "",
            "dagName": dag
        },
        "workflowName": dag
    }
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": keyvault[env]['data_partition_id']
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    if response.status_code == 200:
        response_json = response.json()
        # print(f"{response_json=}")
        return response_json
    elif response.status_code == 409:
        response_json = response.json()
        msg = f"Conflict occurred while registering workflow on data-partition-id={keyvault[env]['data_partition_id']} at {url=}. {response_json.get("message")}"
        return {"msg": msg}
    else:
        msg = f"Error occurred while registering workflows {url=}. {response.text}"
        return {"msg": msg}


def get_workflow_payload(env, data_partition_id, dag, file_id):
    print("Creating Workflow Payload ***************************")
    print(f"{dag=}")
    workflow_payload = {
        "executionContext": {
            "dataPartitionId": f"{data_partition_id}",
            "id": f"{file_id}"
        }
    }
    return workflow_payload


def trigger_workflow(env, data_partition_id, dag, file_id):
    url = f"{keyvault[env]['seds_dns_host']}/api/workflow/v1/workflow/{dag}/workflowRun"

    payload = get_workflow_payload(env, data_partition_id, dag, file_id)

    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition_id
    }

    response = requests.request("POST", url, headers=headers,json=payload)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        msg = f"Error occurred while triggering workflow {url=}. {response.text}"
        return {"msg": msg}
