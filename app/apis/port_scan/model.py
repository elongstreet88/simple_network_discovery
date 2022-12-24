from enum import Enum
from pydantic import BaseModel, Field, root_validator
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)

class PortScanProtocol(str, Enum):
    TCP = "tcp"
    
class PortScan(BaseModel):
    device_address:             str       = Field(description="IP or hostname of device being scanned")
    port:                       int       = Field(description="Port being scanned")
    protocol:                   str       = Field(description="Protocol being scanned.")
    open:                       bool      = Field(default=False, description=f"True if port scan succeed before timeout.")
    scan_duration_ms:           int       = Field(default=0, description="Milliseconds it took to scan the port.")
    scan_max_duration_ms:       int       = Field(default=0, description="Maximum milliseconds allowed to scan the port.")

    class Config:
        schema_extra = {
            "example": {
                "device_address": "google.com",
                "port": 80,
                "protocol": "tcp",
                "open": True,
                "scan_duration_ms": 100,
                "scan_max_duration_ms": 500
            }
        }