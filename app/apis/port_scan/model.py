from enum import Enum
from pydantic import BaseModel, Field
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)

class PortScanProtocol(str, Enum):
    TCP = "tcp"
    
class PortScanSettings(BaseModel):
    timeout:                    int              = Field(default=500, description="Timeout to wait in milliseconds for port scan to complete.")
    protocol:                   PortScanProtocol = Field(default=PortScanProtocol.TCP, description="Protocol to use for port scan.")

class PortScan(BaseModel):
    device_address:             str                 = Field(description="IP or hostname of device being scanned")
    port:                       int                 = Field(description="Port being scanned")
    open:                       bool                = Field(default=False, description=f"True if port scan succeed before timeout.")
    scan_duration:              int                 = Field(default=0, description="Milliseconds it took to scan the port.")
    port_scan_settings:         PortScanSettings    = Field(description="Settings used for port scan.")