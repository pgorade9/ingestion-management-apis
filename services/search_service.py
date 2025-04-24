import asyncio
import json
import uuid
from pathlib import Path

import requests
from starlette.responses import FileResponse

from configuration import keyvault
from models.data_models import SearchQuery
from utils.token_utils import get_token

OUTPUT = "output"


def search_entire_kind(env, data_partition, search_query: SearchQuery):
    DNS_HOST = keyvault[env]["adme_dns_host"]
    BASE_URL = "/api/search/v2/query"

    url = f"{DNS_HOST}{BASE_URL}"
    headers = {
        "data-partition-id": data_partition,
        "Authorization": get_token(env),
        'Content-Type': 'application/json',
    }

    payload = search_query.model_dump()
    print(payload)
    results = []
    limit = 1000
    offset = 0
    try:
        while True:
            params = {
                'offset': limit + offset,
                'limit': limit
            }
            with requests.request('POST', url=url, headers=headers, json=payload, params=params) as response:
                print(f"Sending Search Request with {params=}")
                response_json = response.json()
                if response.status_code == 200:
                    print(f"Search query successful")
                    print(f"{response_json=}")
                    results.append(response_json['results'])
                    offset += limit
                    if len(response_json['results'])<limit:
                        print(len(response_json['results']))
                        break

        search_id = str(uuid.uuid4())
        FILENAME = f"{data_partition}-{search_id}.json"
        PATH = Path(f"{OUTPUT}/{FILENAME}")
        with open(PATH, "w") as fp:
            json.dump(results, fp, indent=4)

        return FileResponse(path=PATH, filename=FILENAME, media_type="application/octet-stream")
        # elif response.status_code == 400:
        #     print(f"Invalid search query.\n{response_json}")
        # elif response.status_code == 403:
        #     print(f"User not authorized to perform the action.\n{response_json}")
    except Exception as e:
        print(f"Error occurred while searching query.\n{e}")


if __name__ == "__main__":
    envs = ["evt", "weu", "sgp", "psc", "eut", "brs"]
    envs_ltops = ["evd-ltops", "evt-ltops", "adme-outerloop", "prod-canary-ltops", "prod-aws-ltops"]

    env = "prod-canary-ltops"
    data_partition = "admedev01-dp4"

    search(env, data_partition)
