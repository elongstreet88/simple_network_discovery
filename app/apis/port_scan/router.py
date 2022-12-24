from fastapi import APIRouter, HTTPException, status, Response
from apis.port_scan.model import PortScan, PortScanProtocol
from apis.port_scan.module import PortScanModule
from tools.tools import FormatJSON
from fastapi_cache.decorator import cache
from starlette.concurrency import run_in_threadpool

# Router info
router = APIRouter(
    prefix                  = "/port_scan",
    tags                    = ["Port Scan"]
)

@router.get("/{protocol}/{device_address}/{port}", response_model=PortScan, status_code=status.HTTP_200_OK)
@cache(expire=1) # 1 Seconds
async def get_port_scan(response:Response, device_address: str, port: int, protocol:PortScanProtocol):
    """
    Checks if a port is open on a device.\n
    Cache: 1 Second
    """
    module = PortScanModule()
    #module.test_udp_port(device_address, port)
    success, results = await run_in_threadpool(module.check_port_open_on_host, device_address, port, protocol)

    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    return results