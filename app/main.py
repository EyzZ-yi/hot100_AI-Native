import os
from fastapi import FastAPI, Header, HTTPException, Depends
from app.routers import practice

_API_KEY = os.getenv("API_KEY")

async def _verify_key(x_api_key: str = Header(None)):
    if _API_KEY and x_api_key != _API_KEY:
        raise HTTPException(403, "forbidden")

app = FastAPI(dependencies=[Depends(_verify_key)])
app.include_router(practice.router)
