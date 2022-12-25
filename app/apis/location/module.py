import requests
from apis.location.model import Location
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)

class LocationModule:
    def get_location(self)->bool|Location:
        """
        Gets location information based on current public IP.

        Returns:
            bool|Location: True if successful, False if failed|Location object with details
        """
        
        # Get public IP
        try:
            response = requests.get('https://api64.ipify.org?format=json').json()
            public_ip = response["ip"]
        except Exception as e:
            logger.warning(f"Unable to get public IP. {e}")
            return False, None

        # Get location info
        try:
            response = requests.get(f'https://ipapi.co/{public_ip}/json/').json()
        except Exception as e:
            logger.warning(f"Unable to get location info. {e}")
            return False, None

        # Parse and return location
        location = Location(
            public_ip       = public_ip,
            city            = response.get("city"),
            region          = response.get("region"),
            country         = response.get("country"),
            latitude        = response.get("latitude"),
            longitude       = response.get("longitude")
        )
        return True, location