import ifcfg
from apis.network_interface.model import NetworkInterface
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)

class NetworkInterfaceModule:
    def get_local_interfaces(self)->bool|list[NetworkInterface]:
        """
        Gets interfaces from the local machine.\n
        Filters out loopback interfaces and interfaces without an ip address.
        Returns True and list of interfaces if successful.
        """

        # Get primary ip address
        #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #s.settimeout(0)
        #try:
        #    # doesn't even have to be reachable
        #    s.connect(('1.1.1.1', 1))
        #    primary_ip = s.getsockname()[0]
        #except Exception:
        #    primary_ip = '127.0.0.1'
        #finally:
        #    s.close()

        # Get interfaces
        try:
            local_interfaces = ifcfg.interfaces()
        except Exception as e:
            logger.warning(f"Unable to get local interfaces, likely due to permissions or 'ifconfig' missing. {e}")
            return True, []
        
        # Filter inetfaces for only those with an ip address
        local_interfaces = {k:v for k,v in local_interfaces.items() if v.get('inet')}

        # Filter out interfaces with 127.0.0.1 inet address
        local_interfaces = {k:v for k,v in local_interfaces.items() if v.get('inet') != '127.0.0.1'}
        
        # Get interface that matches primary ip address
        # primary_interface = {k:v for k,v in local_interfaces.items() if v.get('inet') == primary_ip}

        # Create list of interface models
        results = []
        for interface_name, interface_data in local_interfaces.items():
            interface = NetworkInterface(
                name                = interface_name,
                primary_ip          = interface_data.get('inet'),
                primary_netmask     = interface_data.get('netmask'),
                status              = interface_data.get('status') or "Unknown",
                mac_address         = interface_data.get('ether'),
                data                = interface_data,
            )
            results.append(interface)
        
        # Return results
        return True, results

    def get_local_interface(self, interface_name:str)->bool|NetworkInterface:
        """
        Gets interface from the local machine by name.
        Returns False if interface not found.
        """
            
        # Get interfaces
        success, local_interfaces = self.get_local_interfaces()
        if not success:
            return False, None

        # Filter to interface_name
        local_interfaces = [i for i in local_interfaces if i.name == interface_name]
        if len(local_interfaces) != 1:
            return True, None

        # Return first result
        return True, local_interfaces[0]
