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
