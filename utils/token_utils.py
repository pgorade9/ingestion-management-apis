import requests
from configuration import keyvault


def get_token(env: str):
    if keyvault[env].get("bearer-token") not in [None, ""]:
        return keyvault[env]["bearer-token"]
    scope = f"{keyvault[env]["scope"]} {keyvault[env]["client_id"]}" if env.startswith('ltops') else keyvault[env][
        "scope"]
    response = requests.request(method="POST",
                                url=keyvault[env]["token_url"],
                                headers={"content-type": "application/x-www-form-urlencoded"},
                                data=f"grant_type=client_credentials&client_id={keyvault[env]["client_id"]}&client_secret={keyvault[env]["client_secret"]}&scope={scope}")

    if response.status_code == 200:
        print(f"********* Token Generated Successfully ************")
        response_json = response.json()
        return "Bearer " + response_json["access_token"]
    else:
        print(f"Error occurred while creating token. {response.text}")
        exit(1)
