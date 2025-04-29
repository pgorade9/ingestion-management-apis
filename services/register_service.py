import base64

import requests
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from configuration import keyvault
from models.data_models import CreateSubscriptionPayload, HMACSecret
from utils.token_utils import get_token


def create_subscription(env: str, data_partition: str, topic_name: str, push_endpoint_domain: str, HMAC_Key: str):
    DNS_HOST = keyvault[env]["adme_dns_host"] if push_endpoint_domain == "osdu" else keyvault[env]["seds_dns_host"]
    push_endpoint = f"{DNS_HOST}/api/listener-service/partition/{data_partition}/topic/{topic_name}"
    create_subscription_payload = CreateSubscriptionPayload(description=f"{topic_name} subscription",
                                                            name=topic_name,
                                                            pushEndpoint=push_endpoint,
                                                            secret=HMACSecret(secretType="HMAC", value=HMAC_Key),
                                                            topic=topic_name
                                                            )

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
    elif response.status_code == 409:
        raise HTTPException(status_code=409,
                            detail={"msg": "Conflict Occurred.", "url": url, "headers": headers, "reason": response.text})
    else:
        msg = f"Error occurred while creating subscription using {url=}. {response.status_code=} {response.text}"
        return {"msg": msg}


def get_subscription(env: str, data_partition: str, topic_name: str, push_endpoint_domain: str):
    DNS_HOST = keyvault[env]["adme_dns_host"] if push_endpoint_domain == "osdu" else keyvault[env]["seds_dns_host"]
    push_endpoint = f"{DNS_HOST}/api/listener-service/partition/{data_partition}/topic/{topic_name}"
    subscription_id = base64.b64encode(f"{topic_name}{push_endpoint}".encode()).decode()
    url = f"{keyvault[env]["adme_dns_host"]}/api/register/v1/subscription/{subscription_id}"

    print(f"{subscription_id=}")
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    response = requests.request("GET", url=url, headers=headers, )
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    elif response.status_code == 404:
        raise HTTPException(status_code=404,
                            detail={"msg": "Bad Request.", "url": url, "headers": headers, "reason": response.text})

    else:
        raise HTTPException(status_code=500,
                            detail={"msg": "Error occurred.", "url": url, "headers": headers, "reason": response.text})


def delete_subscription(env: str, data_partition: str, topic_name: str, push_endpoint_domain: str):
    DNS_HOST = keyvault[env]["adme_dns_host"] if push_endpoint_domain == "osdu" else keyvault[env]["seds_dns_host"]
    push_endpoint = f"{DNS_HOST}/api/listener-service/partition/{data_partition}/topic/{topic_name}"
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
        return JSONResponse(status_code=204, content={"msg": msg})

    else:
        msg = f"Error occurred while deleting subscription using {url=}. {response.status_code=} {response.text}"
        return {"msg": msg}
