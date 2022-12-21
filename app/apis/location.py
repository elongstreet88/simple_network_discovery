from fastapi import APIRouter, status, Response
import requests
from models.location import Location
from tools.tools import FormatJSON

router = APIRouter(
    prefix                  = "/location",
    tags                    = ["Location"],
    default_response_class  = FormatJSON
)

@router.get("", response_model=Location, status_code=status.HTTP_200_OK)
async def get_location(response:Response):
    # Get public IP
    response = requests.get('https://api64.ipify.org?format=json').json()
    public_ip = response["ip"]

    # Get location info
    response = requests.get(f'https://ipapi.co/{public_ip}/json/').json()

    # Parse and return location
    location = Location(
        public_ip       = public_ip,
        city            = response.get("city"),
        region          = response.get("region"),
        country         = response.get("country"),
        latitude        = response.get("latitude"),
        longitude       = response.get("longitude")
    )
    return location