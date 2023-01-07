from pydantic import BaseModel, Field

class TCPPortScanSettings(BaseModel):
    tcp_port_scan_timeout:      int                 = Field(default=500, description="Timeout to wait in milliseconds for port scan to complete.", ge=1, le=65535)

class TCPPortScan(BaseModel):
    device_address:             str                 = Field(description="IP or hostname of device being scanned")
    port:                       int                 = Field(description="Port being scanned", ge=1, le=65535)
    open:                       bool                = Field(default=False, description=f"True if port scan succeed before timeout.")
    scan_duration:              int                 = Field(default=0, description="Milliseconds it took to scan the port.")