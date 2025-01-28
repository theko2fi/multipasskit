from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from multipasskit.api.routers import instances, config
from pydantic import BaseModel
import uvicorn
from celery.result import AsyncResult
from multipasskit.api.celerymultipass import celery_app

API_PREFIX = "/api"
VERSION = "v0.1.0"

description = """
This API allows you to manage Multipass instances and resources in a simple, programmatic way using conventional HTTP requests.
"""

app = FastAPI(description=description)

app.include_router(instances.router, prefix=f'{API_PREFIX}/{VERSION}')
app.include_router(config.router, prefix=f'{API_PREFIX}/{VERSION}')

class TaskOut(BaseModel):
    id: str
    status: str

@app.get("/status")
async def status(task_id: str) -> TaskOut:
    r = celery_app.AsyncResult(task_id)
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9990, reload=True, timeout_keep_alive=120)