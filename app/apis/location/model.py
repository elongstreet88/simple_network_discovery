from pydantic import BaseModel, Field
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)
class Location(BaseModel):
    public_ip               : str = Field(description="Current public ip from https")
    city                    : str = Field(description="City from current public ip")
    region                  : str = Field(description="Region from current public ip")
    country                 : str = Field(description="Country from current public ip")
    latitude                : str = Field(description="Latitude from current public ip")
    longitude               : str = Field(description="Longitude from current public ip")