from fastapi import APIRouter, Depends, HTTPException, status, Response
from apis.tcp_port_scan.model import TCPPortScan, TCPPortScanSettings
from apis.tcp_port_scan.module import TCPPortScanModule
from fastapi_cache.decorator import cache

# Router info
router = APIRouter(
    prefix                  = "/tcp_port_scan",
    tags                    = ["TCP Port Scan"]
)

@router.get("/{device_address}/{port}", response_model=TCPPortScan, status_code=status.HTTP_200_OK)
@cache(expire=1) # 1 Seconds
async def get_port_scan(response:Response, device_address: str, port: int, scan_settings:TCPPortScanSettings=Depends()):
    """
    Checks if a port is open on a device.\n
    Cache: 1 second
    """

    # Setup module
    module = TCPPortScanModule()

    # Execute action
    success, results = await module.check_port_open_on_device(
        device_address  = device_address, 
        port            = port
    )

    # Set failed response
    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    # Return results
    return results
