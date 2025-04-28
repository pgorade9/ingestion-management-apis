import uuid
from typing import List

from pydantic import BaseModel


class ResourceValue(BaseModel):
    ResourceValue: str


class StatusPayload(BaseModel):
    correlationId: str = str(uuid.uuid4())
    recordId: str = str(uuid.uuid4())
    recordIdVersion: str = "1.0"
    stage: str = "WORKFLOW"
    status: str = "SUBMITTED"
    message: str = "Workflow execution started"
    errorCode: int = 0
    additionalProperties: dict = {}


class QueryParams(BaseModel):
    correlationId: str = "lightops-evd-4456"
    stage: List[str] = ["WORKFLOW"]


class StatusQuery(BaseModel):
    statusQuery: QueryParams


class SearchQuery(BaseModel):
    kind: str = f"dev-chevron-corporation:test:shapefile:1.0.0"
    query: str = "id:dev-chevron-corporation\\:*\\:*"
    returnedFields: List[str] = ["id", "kind"]
    limit: int = 200


class HMACSecret(BaseModel):
    secretType: str = "HMAC"
    value: str = "ab05fe798f3b2fd13508cb4092c393"


class CreateSubscriptionPayload(BaseModel):
    description: str = "statuschangedtopic subscription"
    name: str = "statuschangedtopic"
    pushEndpoint: str = "https://dataworkflowservices-evd-sdfs.app.evd-2.lightops.slb.com/api/listener-service/partition/admedev01-dp2/topic/statuschangedtopic"
    secret: HMACSecret = {
        "secretType": "HMAC",
        "value": "aec16930cac8e00a354b99e6f5ec88"
    }
    topic: str = "statuschangedtopic"
