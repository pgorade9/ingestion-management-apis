import requests

from configuration import keyvault
from utils.token_utils import get_token


def get_groups(env, data_partition):
    url = f"{keyvault[env]['adme_dns_host']}/api/entitlements/v2/groups"
    querystring = {"type": "DATA", "user": "data.default.owners@qcazadmedev-dp1.dataservices.energy"}
    payload = ""
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    if response.status_code == 200:
        response_json = response.json()
        # print(f"{response_json=}")
        return response_json
    else:
        msg = f"Error occurred while fetching entitlements with {url=}. {response.text}"
        return {"msg": msg}


def get_members_groups(user, env, data_partition, member_type):
    url = f"{keyvault[env]["adme_dns_host"]}/api/entitlements/v2/members/{user}/groups"
    payload = ""
    params = {"type": member_type}
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": data_partition
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        # print(f"{response_json=}")
        return response_json
    else:
        msg = f"Error occurred while fetching member entitlements groups from {url=}. {response.text}"
        return {"msg": msg}


if __name__ == "__main__":
    get_groups("prod-qanoc-ltops")
