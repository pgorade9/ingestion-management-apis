import base64

import requests

from configuration import keyvault
from models.data_models import CreateSubscriptionPayload
from utils.token_utils import get_token


def create_subscription(env:str, data_partition:str, create_subscription_payload: CreateSubscriptionPayload):
    url = f"{keyvault[env]["adme_dns_host"]}/api/register/v1/subscription"
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    payload = create_subscription_payload.model_dump()
    print(f"{payload=}")
    response = requests.request("POST", url=url, headers=headers, json=payload)
    if response.status_code == 201:
        response_json = response.json()
        return response_json
    else:
        msg = f"Error occurred while creating subscription using {url=}. {response.status_code=} {response.text}"
        return {"msg": msg}


def delete_subscription(env:str, data_partition: str, topic_name:str, push_endpoint:str):
    subscription_id = base64.b64encode(f"{topic_name}{push_endpoint}".encode()).decode()
    url = f"{keyvault[env]["adme_dns_host"]}/api/register/v1/subscription/{subscription_id}"
    print(f"{subscription_id=}")
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }

    response = requests.request("DELETE", url=url, headers=headers)
    if response.status_code == 204:
        msg = f"Deleted {topic_name} subscription successfully."
        return {"msg": msg}
        # response_json = response.json()
        # return response_json
    else:
        msg = f"Error occurred while deleting subscription using {url=}. {response.status_code=} {response.text}"
        return {"msg": msg}
