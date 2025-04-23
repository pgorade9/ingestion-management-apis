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


def compare_groups(env_base, data_partition_base,env_test, data_partition_test):
    envs = {env_base:data_partition_base, env_test:data_partition_test}
    groups = {}
    for item in envs.items():
        print(f"{item[0]=}")
        url = f"{keyvault[item[0]]['adme_dns_host']}/api/entitlements/v2/groups"
        querystring = {"type": "DATA", "user": "data.default.owners@qcazadmedev-dp1.dataservices.energy"}
        payload = ""
        headers = {
            "Authorization": get_token(item[0]),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "data-partition-id": item[1]
        }
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            response_json = response.json()
            entitlements = [key['name'] for key in response_json['groups']]
            print(f"{entitlements=}")
            groups[item[0]]=entitlements
        else:
            msg = f"Error occurred while fetching entitlements with {url=}. {response.text}"
            return {"msg": msg}
    group_difference = [item for item in groups[env_base] if item not in groups[env_test]]
    group_difference.sort()
    return group_difference


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
    compare_groups("prod-uscvn-ltops", "dev-chevron-corporation", "prod-euqn-ltops","data")
