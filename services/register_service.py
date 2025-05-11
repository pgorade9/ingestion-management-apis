import base64

import requests
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from configuration import keyvault
from models.data_models import CreateSubscriptionPayload, HMACSecret
from utils.token_utils import get_token


def create_subscription_with_push_endpoint(env: str, data_partition: str, subscription_domain, push_endpoint,
                                           topic_name, HMAC_Key: str):
    create_subscription_payload = CreateSubscriptionPayload(description=f"{topic_name} subscription",
                                                            name=topic_name,
                                                            pushEndpoint=push_endpoint,
                                                            secret=HMACSecret(secretType="HMAC", value=HMAC_Key),
                                                            topic=topic_name
                                                            )
    DNS_HOST = keyvault[env]["adme_dns_host"] if subscription_domain == "osdu" else keyvault[env]["seds_dns_host"]
    url = f"{DNS_HOST}/api/register/v1/subscription"
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
    elif response.status_code in [400, 404, 409]:
        msg = response.json()["message"]
        detail_msg = dict(msg=msg, url=url, payload=payload, headers=headers)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)
    else:
        msg = response.text
        detail_msg = dict(msg=msg, url=url, payload=payload, headers=headers)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)


def create_subscription(env: str, data_partition: str, subscription_domain: str, listener_service_name: str,
                        topic_name: str,
                        push_endpoint_namespace: str, HMAC_Key: str):
    REGISTER_SERVICE_DNS_HOST = keyvault[env]["adme_dns_host"] if subscription_domain == "osdu" else keyvault[env][
        "seds_dns_host"]
    url = f"{REGISTER_SERVICE_DNS_HOST}/api/register/v1/subscription"

    PUSH_ENDPOINT_DNS_HOST = keyvault[env]["dw_dns_host"] if push_endpoint_namespace == "dw" else keyvault[env][
        "seds_dns_host"]
    base_path = f"/dm/{listener_service_name}/events/v1/statusTopic/{data_partition}" if push_endpoint_namespace == "dw" else f"/api/{listener_service_name}/partition/{data_partition}/topic/{topic_name}"
    push_endpoint = f"{PUSH_ENDPOINT_DNS_HOST}{base_path}"
    create_subscription_payload = CreateSubscriptionPayload(description=f"{topic_name} subscription",
                                                            name=topic_name,
                                                            pushEndpoint=push_endpoint,
                                                            secret=HMACSecret(secretType="HMAC", value=HMAC_Key),
                                                            topic=topic_name)

    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    payload = create_subscription_payload.model_dump()
    # detail_msg = dict(url=url, payload=payload, headers=headers)
    # return detail_msg
    response = requests.request("POST", url=url, headers=headers, json=payload)
    if response.status_code == 201:
        response_json = response.json()
        return response_json
    elif response.status_code in [400, 404, 409]:
        msg = response.json()["message"]
        detail_msg = dict(msg=msg, url=url, payload=payload, headers=headers)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)
    else:
        msg = response.text
        detail_msg = dict(msg=msg, url=url, payload=payload, headers=headers)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)


def get_subscription(env: str, data_partition: str, subscription_domain: str, listener_service_name: str,
                     topic_name: str, push_endpoint_namespace: str):
    PUSH_ENDPOINT_DNS_HOST = keyvault[env]["dw_dns_host"] if push_endpoint_namespace == "dw" else keyvault[env][
        "seds_dns_host"]
    base_path = f"/dm/{listener_service_name}/events/v1/statusTopic/{data_partition}" if push_endpoint_namespace == "dw" else f"/api/{listener_service_name}/partition/{data_partition}/topic/{topic_name}"
    push_endpoint = f"{PUSH_ENDPOINT_DNS_HOST}{base_path}"

    REGISTER_SERVICE_DNS_HOST = keyvault[env]["adme_dns_host"] if subscription_domain == "osdu" else keyvault[env][
        "seds_dns_host"]
    subscription_id = base64.b64encode(f"{topic_name}{push_endpoint}".encode()).decode()
    url = f"{REGISTER_SERVICE_DNS_HOST}/api/register/v1/subscription/{subscription_id}"

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
    elif response.status_code in [400, 404, 409]:
        msg = response.json()["message"]
        detail_msg = dict(msg=msg, url=url, headers=headers)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)
    else:
        msg = response.text
        detail_msg = dict(msg=msg, url=url, headers=headers)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)


def get_subscription_notification_id(env: str, data_partition: str, notification_id: str):
    url = f"{keyvault[env]["seds_dns_host"]}/api/register/v1/subscription"

    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    params = {
        "notificationId": notification_id
    }
    response = requests.request("GET", url=url, headers=headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    elif response.status_code in [400, 404, 409]:
        msg = response.json()["message"]
        detail_msg = dict(msg=msg, url=url, headers=headers)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)
    else:
        msg = response.text
        detail_msg = dict(msg=msg, url=url, headers=headers)
        raise HTTPException(status_code=500, detail=detail_msg)


def delete_subscription(env: str, data_partition: str, listener_service_name: str, topic_name: str,
                        push_endpoint_domain: str):
    DNS_HOST = keyvault[env]["adme_dns_host"] if push_endpoint_domain == "osdu" else keyvault[env]["seds_dns_host"]
    push_endpoint = f"{DNS_HOST}/api/{listener_service_name}/partition/{data_partition}/topic/{topic_name}"
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


def update_secret(hmac_secret: HMACSecret, env: str, data_partition: str, listener_service_name: str, topic_name: str,
                  push_endpoint_domain: str):
    DNS_HOST = keyvault[env]["adme_dns_host"] if push_endpoint_domain == "osdu" else keyvault[env]["seds_dns_host"]
    push_endpoint = f"{DNS_HOST}/api/{listener_service_name}/partition/{data_partition}/topic/{topic_name}"
    subscription_id = base64.b64encode(f"{topic_name}{push_endpoint}".encode()).decode()
    url = f"{keyvault[env]["adme_dns_host"]}/api/register/v1/subscription/{subscription_id}"

    print(f"{subscription_id=}")
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    payload = hmac_secret.model_dump()
    response = requests.request("PUT", url=url, headers=headers, json=payload)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    elif response.status_code in [400, 404, 409]:
        msg = response.json()["message"]
        detail_msg = dict(msg=msg, url=url, payload=payload, headers=headers)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)
    else:
        msg = response.text
        detail_msg = dict(msg=msg, url=url, payload=payload, headers=headers)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)


def validate_push_endpoint(env, data_partition, push_endpoint, crc, hmac_key):
    url = push_endpoint
    headers = {
        "Authorization": get_token(env),
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    params = {
        "crc": crc,
        "hmac": hmac_key
    }
    response = requests.request("GET", url=url, headers=headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    elif response.status_code in [400, 404, 409]:
        msg = response.text
        detail_msg = dict(msg=msg, url=url, headers=headers, params=params)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)
    else:
        msg = response.text
        detail_msg = dict(msg=msg, url=url, headers=headers, params=params)
        raise HTTPException(status_code=response.status_code, detail=detail_msg)
