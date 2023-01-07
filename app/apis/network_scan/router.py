from fastapi import APIRouter, HTTPException, status, Response
from fastapi_cache.decorator import cache
from apis.network_scan.model import NetworkScan, NetworkScanSettings
from apis.network_scan.module import NetworkScanModule
from fastapi import Depends

# Router info
router = APIRouter(
    prefix                  = "/network_scan",
    tags                    = ["Network Scan"]
)

@router.get("/{address}/{mask}", response_model=NetworkScan, status_code=status.HTTP_200_OK)
@cache(expire=1) # 1 Seconds
async def get_network_scan(response:Response, address: str, mask:str, network_scan_settings: NetworkScanSettings=Depends()):
    """
    Scan all devices on a network.\n
    Includes ping scan and port scan.\n
    Cache: 1 Second
    """

    module = NetworkScanModule()
    success, results = await module.scan_network(
        network_address         = f"{address}/{mask}", 
        network_scan_settings   = network_scan_settings
    )

    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    return results
