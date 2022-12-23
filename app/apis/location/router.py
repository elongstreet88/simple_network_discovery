from fastapi import APIRouter, HTTPException, status, Response
from apis.location.model import Location
from apis.location.module import LocationModule
from tools.tools import FormatJSON
from starlette.concurrency import run_in_threadpool
from fastapi_cache.decorator import cache

# Router info
router = APIRouter(
    prefix                  = "/location",
    tags                    = ["Location"],
    default_response_class  = FormatJSON
)

@router.get("", response_model=Location, status_code=status.HTTP_200_OK)
@cache(expire=60) #1 Minute
async def get_location(response:Response):
    module = LocationModule()
    success, results = await run_in_threadpool(module.get_location)

    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail      = f"Bad request."
        )

    return results