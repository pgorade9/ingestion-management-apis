import uvicorn
from fastapi import FastAPI
from apis.entitlements import ent_router
from apis.legal_tags import legal_router
from apis.workflow import workflow_router

app = FastAPI(title="ingestion-management")

app.include_router(ent_router)
app.include_router(workflow_router)
app.include_router(legal_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=9001)
