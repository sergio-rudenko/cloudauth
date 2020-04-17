from fastapi import APIRouter, Header, HTTPException

from app import conf

router = APIRouter()


# path
@router.get("/")
async def get_path():
    return {"path": f"{conf.api_prefix}", "version": f"{conf.api_version}"}


# test route
@router.get("/test")
async def get_message(x_token: str = Header(...)):
    if not x_token:
        raise HTTPException(status_code=401, detail="token required")
    return {"message": "Hello, World!"}
