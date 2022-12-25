from enum import Enum
from pydantic import BaseModel, Field, root_validator
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)

class PingScanSettings(BaseModel):
    size:                       int       = Field(default=1, description="Size of packet to send")
    timeout:                    int       = Field(default=2, description="Timeout in seconds")
    count:                      int       = Field(default=4, description="Number of packets to send")
    interval:                   int       = Field(default=0, description="Interval between packets in seconds")

class PingScan(BaseModel):
    device_address:             str              = Field(description="IP or hostname of device being scanned")
    online:                     bool             = Field(default=False,description="True if device successfully completed all ping requests")
    average_rtt:                float            = Field(default=0, description="Average round trip time in milliseconds")
    jitter:                     float            = Field(default=0, description="Jitter in milliseconds")
    max_rtt:                    float            = Field(default=0, description="Maximum round trip time in milliseconds")
    min_rtt:                    float            = Field(default=0, description="Minimum round trip time in milliseconds")
    packets_sent:               int              = Field(default=0, description="Number of packets sent")
    packets_received:           int              = Field(default=0, description="Number of packets received")
    packet_loss:                float            = Field(default=0, description="Percentage of packets lost")
    ping_scan_settings:         PingScanSettings = Field(description="Settings for ping scan")
