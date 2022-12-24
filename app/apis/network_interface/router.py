from fastapi import APIRouter, HTTPException, status, Response
from apis.network_interface.module import NetworkInterfaceModule
from apis.network_interface.model import NetworkInterface
from tools.tools import FormatJSON
from fastapi_cache.decorator import cache

# Router info
router = APIRouter(
    prefix                  = "/network_interface",
    tags                    = ["Network Interface"]
)

@router.get("", response_model=list[NetworkInterface], status_code=status.HTTP_200_OK)
@cache(expire=60) #1 Minute
async def get_network_interfaces(response:Response):
    """
    Gets network interfaces from the local machine.\n
    Filters out loopback interfaces and interfaces without an ip address. \n
    Cache: 1 Minute
    """
    core = NetworkInterfaceModule()
    success, results = core.get_local_interfaces()

    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    return results


@router.get("/{network_interface_name}", response_model=NetworkInterface, status_code=status.HTTP_200_OK)
@cache(expire=60) #1 Minute
async def get_network_interface(network_interface_name:str):
    """
    Gets interface from the local machine by name.\n
    Cache: 1 Minute
    """

    core = NetworkInterfaceModule()
    success, results = core.get_local_interface(network_interface_name)

    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    # Set Status to 404 if results not found
    if not results:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail      = f"Resource does not exist."
        )

    return results