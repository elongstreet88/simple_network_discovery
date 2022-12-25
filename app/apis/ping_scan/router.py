from fastapi import APIRouter, HTTPException, status, Response
from fastapi_cache.decorator import cache
from starlette.concurrency import run_in_threadpool
from apis.ping_scan.model import PingScan, PingScanSettings
from apis.ping_scan.module import PingScanModule
from fastapi import Depends

# Router info
router = APIRouter(
    prefix                  = "/ping_scan",
    tags                    = ["Ping Scan"]
)

@router.get("/{device_address}", response_model=PingScan, status_code=status.HTTP_200_OK)
@cache(expire=1) # 1 Seconds
async def get_ping_scan(response:Response, device_address: str, ping_scan_settings: PingScanSettings=Depends()):
    """
    Check if a device is online using ping scan.
    Cache: 1 Second
    """

    module = PingScanModule()
    success, results = await run_in_threadpool(module.ping_device, device_address, ping_scan_settings)

    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    return results