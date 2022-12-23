import ipaddress
import typing
from pydantic import BaseModel, Field, root_validator
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)

class NetworkInterface(BaseModel):
    name:                   str  = Field(description="Interface name. Ex: eth0")
    primary_ip:             str  = Field(description="Primary IP address. Ex: 192.168.0.1")
    primary_netmask:        str  = Field(description="Primary netmask. Ex: 255.255.255.0")
    primary_network:        str  = Field(default=None, description="Primary network. Ex: 192.168.0.0")
    primary_network_cidr:   str  = Field(default=None, description="Primary network CIDR. Ex: 192.168.0.0/24")
    status:                 str  = Field(description="Interface status. Ex: active")
    mac_address:            str  = Field(description="MAC address")
    data:                   dict = Field(description="Interface data")

    @root_validator
    def root_validator(cls, values) -> typing.Dict:
        # Get the network address from the primary IP and netmask
        try:
            # Parse network
            network = ipaddress.IPv4Network(f"{values['primary_ip']}/{values['primary_netmask']}", strict=False)

            # Calculate additional network values
            values['primary_network']       = str(network.network_address)
            values['primary_network_cidr']  = str(network.with_prefixlen)
        except Exception as e:
            logger.warning(f"Invalid IP address or netmask: [{values}]. {e}")
            raise ValueError("Invalid IP address or netmask.")

        # Return all values
        return values