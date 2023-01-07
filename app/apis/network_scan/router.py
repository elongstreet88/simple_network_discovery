from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache
from apis.network_scan.model import NetworkScan, NetworkScanSettings
from apis.network_scan.module import NetworkScanModule
from fastapi import Depends

# Router info
router = APIRouter(
    prefix                  = "/network_scan",
    tags                    = ["Network Scan"]
)

@router.get("", response_model=NetworkScan, status_code=status.HTTP_200_OK)
@cache(expire=60) # 1 Minute
async def get_network_scan():
    """
    Scan all devices on the local network.\n
    Note - This only gets the first local interface and scans the network associated with that interface.\n
    Cache: 1 Minute
    """
    module  = NetworkScanModule()
    success, results = await module.scan_local_primary_interface_network()

    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    return results

@router.get("/{address}/{mask}", response_model=NetworkScan, status_code=status.HTTP_200_OK)
@cache(expire=60) # 1 Minute
async def get_network_scan(address: str, mask:str, network_scan_settings: NetworkScanSettings=Depends()):
    """
    Scan all devices on a network.\n
    Includes ping scan and port scan.\n
    Cache: 1 Minute
    """

    module = NetworkScanModule(network_scan_settings = network_scan_settings)
    success, results = await module.scan_network(
        network_address         = f"{address}/{mask}"
    )

    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    return results
