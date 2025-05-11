from fastapi import FastAPI
from redis import Redis
import httpx

from .scheduler import start_scheduler
from app.api_v1.views import router_v1

app = FastAPI()
app.include_router(router_v1)

start_scheduler()

@app.on_event("startup")
async def startup_event():
    app.state.redis = Redis(host='localhost', port=6379)
    app.state.http_client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()

