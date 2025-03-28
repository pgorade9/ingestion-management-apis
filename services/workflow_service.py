import requests

from configuration import keyvault
from utils.token_utils import get_token


def get_workflows(env):
    url = f"{keyvault[env]['seds_dns_host']}/api/workflow/v1/workflow"
    payload = ""
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": keyvault[env]['data_partition_id']
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        # print(f"{response_json=}")
        return response_json
    else:
        msg = f"Error occurred while fetching workflows {url=}. {response.text}"
        return {"msg": msg}


def get_workflow(env, dag):
    url = f"{keyvault[env]['seds_dns_host']}/api/workflow/v1/workflow/{dag}"
    payload = ""
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": keyvault[env]['data_partition_id']
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
        "description": f"{desc[dag]}",
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
        print(f"{response_json=}")
        return response_json
    elif response.status_code == 409:
        response_json = response.json()
        msg = f"Conflict occurred while registering workflow on data-partition-id={keyvault[env]['data_partition_id']} at {url=}. {response_json.get("message")}"
        return {"msg": msg}
    else:
        msg = f"Error occurred while registering workflows {url=}. {response.text}"
        return {"msg": msg}
