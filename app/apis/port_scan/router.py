from fastapi import APIRouter, Depends, HTTPException, status, Response
from apis.port_scan.model import PortScan, PortScanSettings
from apis.port_scan.module import PortScanModule
from fastapi_cache.decorator import cache
from starlette.concurrency import run_in_threadpool

# Router info
router = APIRouter(
    prefix                  = "/port_scan",
    tags                    = ["Port Scan"]
)

@router.get("/{device_address}/{port}", response_model=PortScan, status_code=status.HTTP_200_OK)
@cache(expire=1) # 1 Seconds
async def get_port_scan(response:Response, device_address: str, port: int, scan_settings:PortScanSettings=Depends()):
    """
    Checks if a port is open on a device.\n
    Cache: 1 second
    """
    module = PortScanModule()
    success, results = await run_in_threadpool(module.check_port_open_on_device, device_address, port, scan_settings)

    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    return results
