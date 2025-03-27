import json
import requests

from configuration import keyvault


def get_token(env: str):
    scope = f"{keyvault[env]["scope"]} {keyvault[env]["client_id"]}" if env.startswith('ltops') else keyvault[env][
        "scope"]
    response = requests.request(method="POST",
                                url=keyvault[env]["token_url"],
                                headers={"content-type": "application/x-www-form-urlencoded"},
                                data=f"grant_type=client_credentials&client_id={keyvault[env]["client_id"]}&client_secret={keyvault[env]["client_secret"]}&scope={scope}")

    if response.status_code == 200:
        print(f"********* Token Generated Successfully ************")
        response_dict = json.loads(response.text)
        return "Bearer " + response_dict["access_token"]
    else:
        print(f"Error occurred while creating token. {response.text}")
        # exit(1)


def get_groups(env):
    url = f"{keyvault[env]['adme_dns_host']}/api/entitlements/v2/groups"
    querystring = {"type": "DATA", "user": "data.default.owners@qcazadmedev-dp1.dataservices.energy"}
    payload = ""
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": keyvault[env]['data_partition_id']
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    if response.status_code == 200:
        response_json = response.json()
        print(f"{response_json=}")
        return response_json
    else:
        print(f"Error occurred while fetching entitlements. {response.text}")
        # exit(1)


def get_members_groups(user, env, member_type):
    url = f"{keyvault[env]["adme_dns_host"]}/api/entitlements/v2/members/{user}/groups"
    payload = ""
    params = {"type": member_type}
    headers = {
        "Authorization": get_token(env),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "data-partition-id": keyvault[env]['data_partition_id']
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        print(f"{response_json=}")
        return response_json
    else:
        print(f"Error occurred while fetching member entitlements groups from {url=}. {response.text}")
        # exit(1)


if __name__ == "__main__":
    get_groups("prod-qanoc-ltops")
