from fastapi import Depends, FastAPI
from pydantic import BaseModel
from logs.logs import get_logger
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from apis.location.router import router as location_router
from apis.network_interface.router import router as network_interface_router
from apis.tcp_port_scan.router import router as tcp_port_scan_router
from apis.ping_scan.router import router as ping_scan_router
from apis.network_scan.router import router as network_scan_router
from fastapi import FastAPI, Query
from typing import List

# Root vars
root_path   = "/api"
api_title   = "Simple Network Discovery"

# Setup logger using defaults
logger = get_logger(__name__)

# Fast API
app = FastAPI(
    title       = api_title,
    description = api_title
)
    
# Register Routes
app.include_router(location_router,             prefix=root_path)
app.include_router(network_interface_router,    prefix=root_path)
app.include_router(tcp_port_scan_router,        prefix=root_path)
app.include_router(ping_scan_router,            prefix=root_path)
app.include_router(network_scan_router,         prefix=root_path)

@app.on_event("startup")
async def startup():
    # Enable Caching
    FastAPICache.init(InMemoryBackend())

# Redirect to docs (only useful when debugging locally)
@app.get("/")
async def root():
    return "Welcome"

@app.get("/health")
async def health():
    """
    Return status code 200 OK if healthy.
    """
    return "OK"