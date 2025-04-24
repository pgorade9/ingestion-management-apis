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
