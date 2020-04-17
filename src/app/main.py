import os
import time

from typing import List
from fastapi import FastAPI, Request, Header, HTTPException
from uvicorn.main import Server

from app import models
from app.data import engine
from app import conf

from app.api.default import router as default_router
from app.api.crud import router as crud_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    version=conf.version,
    title=conf.title,
    description="Service to store data from MQTT device topic to Postgres database",
    redoc_url=f'{conf.api_prefix}/redoc',
    docs_url=f'{conf.api_prefix}/docs',
    openapi_prefix=os.getenv('SERVICE_PREFIX', '/cloudauth')
)


# https://fastapi.tiangolo.com/tutorial/middleware/
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # TODO: dirty check 'X-Token'
    # print("request:", request.headers)
    # if 'x-token' not in request.headers:
    #     response = Response(
    #         status_code=401,
    #         content='{"detail": "read the docs, provide token"}',
    #         media_type="application/json"
    #     )
    #     return response
    #
    # if request.headers['x-token'] != '11223344':
    #     response = Response(
    #         status_code=401,
    #         content='{"detail": "token is not valid"}',
    #         media_type="application/json"
    #     )
    #     return response

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    if 'x-token' in request.headers:
        response.headers["X-Token-Received"] = request.headers['x-token']
    else:
        response.headers["X-Token-Received"] = "none"

    return response


@app.on_event("startup")
async def startup():
    print("app::event: startup")
    return None


@app.on_event("shutdown")
async def shutdown():
    print("app::event: shutdown")
    return None


app.include_router(default_router, tags=["default"])
app.include_router(crud_router, prefix=f'{conf.api_prefix}')
