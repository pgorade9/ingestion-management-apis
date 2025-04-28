import requests

from configuration import keyvault
from models.data_models import StatusPayload, StatusQuery
from utils.token_utils import get_token


def publish_status(env: str, data_partition: str, status: StatusPayload):
    url = f"{keyvault[env]['seds_dns_host']}/api/status-publisher/v1/status"

    payload = [
        status.model_dump()
    ]
    # print(f"{payload=}")
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    if response.status_code == 200:
        msg = f"Published Message Successfully on {data_partition}"
    elif response.status_code in [i for i in range(400, 500)]:
        response_json = response.json()
        msg = f"Bad Request for {url=}. {response_json=}"
    else:
        msg = f"Error occurred while publishing status {url=}. {response.text}"
    return {"msg": msg}


def get_status(env: str, data_partition: str, status_filter: StatusQuery):
    url = f"{keyvault[env]['seds_dns_host']}/api/status-processor/v1/status/query"

    payload = status_filter.model_dump()
    print(f"{payload=}")
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    elif response.status_code in [i for i in range(400, 500)]:
        response_json = response.json()
        msg = f"Bad Request for {url=}. {response_json=}"
        return {"msg": msg}
    else:
        msg = f"Error occurred while publishing status {url=}. {response.text}"
        return {"msg": msg}
