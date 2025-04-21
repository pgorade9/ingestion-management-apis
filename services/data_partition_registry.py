import requests

from configuration import keyvault
from utils.token_utils import get_token


def fetch_resource(region, env, data_partition, app_code, resource_key):
    DNS_HOST = "api.delfi.slb.com" if region == "us" else "eu-api.delfi.slb.com"
    url = f"https://{DNS_HOST}/ccm/dataPartitionRegistry/v2/dataPartitions/{data_partition}/applications/{app_code}/resources/{resource_key}"
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition,
        "appkey": keyvault["prod-api-key"]
    }

    response = requests.request("GET", url=url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        msg = f"Error occurred while fetching member entitlements groups from {url=}. {response.status_code=} {response.text}"
        return {"msg": msg}


def fetch_resources(region, env, data_partition, app_code):
    DNS_HOST = "api.delfi.slb.com" if region == "us" else "eu-api.delfi.slb.com"
    url = f"https://{DNS_HOST}/ccm/dataPartitionRegistry/v2/dataPartitions/{data_partition}/applications/{app_code}/resources"
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition,
        "appkey": keyvault["prod-api-key"]
    }
    print(f"{headers=}")
    response = requests.request("GET", url=url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        msg = f"Error occurred while fetching member entitlements groups from {url=}. {response.status_code=} {response.text}"
        return {"msg": msg}


def create_resource(resource, region, env, data_partition, app_code, resource_key):
    DNS_HOST = "api.delfi.slb.com" if region == "us" else "eu-api.delfi.slb.com"
    url = f"https://{DNS_HOST}/ccm/dataPartitionRegistry/v2/dataPartitions/{data_partition}/applications/{app_code}/resources/{resource_key}"
    print(f"{resource=}")
    payload = resource.dict()

    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition,
        "appkey": keyvault["prod-api-key"]
    }
    response = requests.request("PUT", url=url, headers=headers, json=payload)
    if response.status_code == 200:
        response_json = response.json()
        print(f"{response_json=}")
        return response_json
    else:
        msg = f"Error occurred while updating resource key at {url=}. {response.status_code=} {response.text}"
        print(f"{msg=}")
        return {"msg": msg}
