import requests

from configuration import keyvault
from utils.token_utils import get_token


def get_legal_tags(env):
    url = f"{keyvault[env]['adme_dns_host']}/api/legal/v1/legaltags"
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