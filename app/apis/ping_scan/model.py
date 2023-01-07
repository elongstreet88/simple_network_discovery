from pydantic import BaseModel, Field
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)

class PingScanSettings(BaseModel):
    ping_scan_size:        int       = Field(default=1, description="Size of packet to send", ge=1, le=65507)
    ping_scan_timeout:     int       = Field(default=2, description="Timeout in seconds", ge=1, le=60)
    ping_scan_count:       int       = Field(default=4, description="Number of packets to send", ge=1, le=100)
    ping_scan_interval:    int       = Field(default=0, description="Interval between packets in seconds", ge=0, le=60)

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