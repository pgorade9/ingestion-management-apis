import requests

from configuration import keyvault
from utils.token_utils import get_token


def get_role_assignments(region, env, billing_account_id, contract_id, app_code):
    DNS_HOST = "api.delfi.slb.com" if region == "us" else "eu-api.delfi.slb.com"
    url = f"https://{DNS_HOST}/ccm/userAssociation/v1/roleAssignments?billingAccountId={billing_account_id}&contractId={contract_id}&appCode={app_code}"
    headers = {
        "Authorization": get_token(env),
        "Accept": "application/json",
        "appkey": keyvault["prod-api-key"],

    }

    params = {
        'billingAccountId': billing_account_id,
        'contractId': contract_id,
        'appCode': app_code
    }
    print(f"{headers=}{params=}")
    response = requests.request("GET", url=url, headers=headers)
    if response.status_code == 200:
        print(f"{response.url=}")
        response_json = response.json()
        print(f"{url=}")
        print(response_json)
        return response_json
    else:
        msg = f"Error occurred while fetching user role assignments groups from {url=}. {response.status_code=} {response.text}"
        return {"msg": msg}


if __name__ == "__main__":
    get_role_assignments("us","prod-canary-ltops", "DIGITAL2020", "2T6DR4TH1T", "datamanager")
