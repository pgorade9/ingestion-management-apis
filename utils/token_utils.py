import requests

from configuration import keyvault


def get_token(env: str):
    if keyvault.get(env).get("bearer-token") not in [None, ""]:
        return keyvault[env]["bearer-token"]
    scope_osdu = keyvault[env]["scope"]
    scope_client_id = keyvault[env]["client_id"]
    scope_ccm = keyvault["scope_ccm"]
    scope = f"{scope_osdu} {scope_client_id} {scope_ccm}" if env.endswith('ltops') else keyvault[env][
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
        msg = f"Error occurred while fetching token from {keyvault[env]["token_url"]=}. {response.status_code=} {response.text}"
        print(f"{msg=}")
