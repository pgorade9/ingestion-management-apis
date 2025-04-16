import base64

import requests

from configuration import keyvault
from utils.token_utils import get_token


def get_session(env: str, data_partition_id: str, user_id: str):
    if keyvault.get(env).get("bearer-token") not in [None, ""]:
        return keyvault[env]["bearer-token"]

    url = f"{keyvault[env]['seds_dns_host']}/api/workflow/v1/workflow/getSession"

    headers = {
        "content-type": "application/json",
        "sToken": base64.b64encode(f"{user_id}:{keyvault[env]['client_id']}:3600".encode("utf-8")).decode("utf-8"),
        "data-partition-id": data_partition_id,
        "secretAuthorization": f"Basic {base64.b64encode(f"{keyvault[env]['client_id']}:{keyvault[env]['client_secret']}".encode("utf-8")).decode("utf-8")}",
        # "audience": f"{keyvault[env]['client_id']} {keyvault[env]['scope']}",
        "Authorization": get_token(env),
        "requestUrl": f"{keyvault[env]['adme_dns_host']}"
    }
    print(f"{headers=}")
    response = requests.request(method="GET",
                                url=url,
                                headers=headers)

    if response.status_code == 200:
        print(f"********* Token Generated Successfully ************")
        response_json = response.json()
        return response_json
    else:
        msg = f"Error occurred while fetching from get Session endpoint from {url}. {response.status_code=} {response.text}"
        print(f"{msg=}")


def get_endpoint_id(env:str, data_partition: str):
    url = f"https://api.delfi.slb.com/ccm/dataPartitionList/v2/dataPartitions/{data_partition}"

    headers = {
        "accept": "application/json",
        "appkey": "slAxZPVhPSTH9Ij45Rm6noymBgj4pQpZ",
        "Authorization": get_token(env)
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        print(f"{response_json=}")
        endpoint_id = response_json.get("endpointId")

        return response_json
    else:
        print(f"Error occurred. {response.status_code=} {response.text=} {url=}")


def get_resource_id(env, endpoint_id):
    url = f"https://api.delfi.slb.com/ccm/endpointRegistry/v1/dataDeployments/{endpoint_id}"
    payload = ""
    headers = {
        "accept": "application/json",
        "appkey": "slAxZPVhPSTH9Ij45Rm6noymBgj4pQpZ",
        "Authorization": get_token(env)
    }

    response = requests.request("GET", url, data=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        resource_id = response_json.get("resource").get("resourceId")
        print(f"{resource_id=}")
        return response_json
    else:
        print(f"{response=}")


def exchange_token(env, resource_id):
    subject_token = get_token(env).split()[1]
    payload = f"grant_type=token-exchange&subject_token={subject_token}&subject_token_type=urn:ietf:params:oauth:token-type:access_token&requested_token_type=urn:ietf:params:oauth:token-type:access_token&resource={resource_id}"
    encoded_secret = f'{keyvault[env]["client_id"]}:{keyvault[env]["client_secret"]}'.encode("utf-8")
    response = requests.request(method="POST",
                                url="https://csi.slb.com/v2/token",
                                headers={"content-type": "application/x-www-form-urlencoded",
                                         "Authorization": f"Basic {base64.b64encode(encoded_secret).decode('utf-8')}"},
                                data=payload)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        print(f"Error occurred. {response.status_code=} {response.text=}")
