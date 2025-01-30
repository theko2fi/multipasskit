from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from multipasskit.api.routers import instances, config
from pydantic import BaseModel
from celery.result import AsyncResult
from multipasskit.api.celerymultipass import celery_app
from multipasskit.api.config import settings

API_PREFIX = "/api"

description = """
This API allows you to manage Multipass instances and resources in a simple, programmatic way using conventional HTTP requests.
"""

app = FastAPI(
    title=settings.APP_NAME,
    description=description
)

app.include_router(instances.router, prefix=f'{API_PREFIX}/{settings.MULTIPASS_API_VERSION}')
app.include_router(config.router, prefix=f'{API_PREFIX}/{settings.MULTIPASS_API_VERSION}')

class TaskOut(BaseModel):
    id: str
    status: str

@app.get("/tasks/{id}/status", tags=["celery"], response_model=TaskOut)
async def status(id: str) -> TaskOut:
    r = celery_app.AsyncResult(id)
    return _to_task_out(r)

def _to_task_out(r: AsyncResult) -> TaskOut:
    return TaskOut(id=r.task_id, status=r.status)

@app.middleware("http")
async def middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})