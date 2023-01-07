from fastapi import Depends
from pydantic import BaseModel, Field
from apis.ping_scan.model import PingScan, PingScanSettings
from apis.tcp_port_scan.model import TCPPortScan, TCPPortScanSettings
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)

class Device(BaseModel):
    ip_address:             str              = Field(description="IP address of device")
    mac_address:            str              = Field(description="MAC address of device")
    hostname:               str              = Field(description="Hostname of device")

class NetworkScan(BaseModel):
    network:                    str                 = Field(description="Network address being scanned. Ex: 192.168.0.0/24")
    ping_scan_results:          list[PingScan]      = Field(default=[],description="List of ping scan results")
    tcp_port_scan_results:      list[TCPPortScan]   = Field(default=[],description="List of port scan results")

class NetworkScanSettings(BaseModel):
    tcp_port_scan_settings:     TCPPortScanSettings = Depends()
    ping_scan_settings:         PingScanSettings    = Depends()
    tcp_port_scan_range:        str                 = Field(default="21-23,25,53,80,110,123,143,443,445,993,995,1723,3306,3389,5900,8080", description="Port range to scan in string format. Ex: '1-53,80,443'")