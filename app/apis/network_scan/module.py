from apis.network_scan.model import NetworkScan, NetworkScanSettings
from apis.ping_scan.module import PingScanModule
from apis.tcp_port_scan.module import TCPPortScanModule
from logs.logs import get_logger
import ipaddress
import asyncio

# Setup logger using defaults
logger = get_logger(__name__)

class NetworkScanModule:
    async def scan_network(self, network_address:str, network_scan_settings:NetworkScanSettings)->bool|NetworkScan:
        """_summary_

        Args:
            network_address (str): Network address to scan. Ex: 192.168.0.0/24
            network_scan_settings (NetworkScanSettings): Settings for network scan
            port_scan_ports (list[int], optional): List of ports to scan. Defaults to DEFAULT_PORT_SCAN_PORTS.

        Returns:
            bool|NetworkScan: True if successful, False if not. NetworkScan object if successful, None if not.
        """

        # Verify network address
        network = None
        try:
            network = ipaddress.ip_network(network_address)
        except:
            logger.error(f"Invalid network address: {network_address}")
            return False, None

        # Result object
        network_scan = NetworkScan(network=network_address)

        # Get usable ips in network
        ips = list(network.hosts())

        # Ping scan each ip
        ping_scan_module = PingScanModule(
            ping_scan_settings          = network_scan_settings.ping_scan_settings,
            max_concurrent_connections  = 64
        )
        tasks = []
        for ip in ips:
            tasks.append(asyncio.create_task(ping_scan_module.ping_device(str(ip))))

        for task in tasks:
            success, ping_scan_result = await task
            if success and ping_scan_result.online:
                network_scan.ping_scan_results.append(ping_scan_result)

        # Get list of ports to scan
        success, port_scan_ports = self.port_string_to_port_list(network_scan_settings.tcp_port_scan_range)
        if not success:
            logger.info(f"Invalid port range: {network_scan_settings.tcp_port_scan_range}")
            return False, None

        # Create asyncio tasks for port scan
        port_scan_modeule = TCPPortScanModule(
            max_concurrent_connections  = 64,
            port_scan_settings          = network_scan_settings.tcp_port_scan_settings
        )
        tasks = []
        for ping_scan_result in network_scan.ping_scan_results:
            for port in port_scan_ports:
                tasks.append((port_scan_modeule.check_port_open_on_device(
                    ping_scan_result.device_address, 
                    port
                )))

        # Run port scan tasks
        print(len(tasks))
        results = await asyncio.gather(*tasks)

        # Add port scan results to network scan
        for result in results:
            success, port_scan_result = result
            if success and port_scan_result.open:
                network_scan.tcp_port_scan_results.append(port_scan_result)
            
        return True, network_scan

    def port_string_to_port_list(self, port_string:str)->bool|list[int]:
        """_summary_

        Args:
            port_string (str): Port range to scan in string format. Ex: '1-53,80,443'

        Returns:
            bool|list[int]: True if successful, False if not. List of ports if successful, None if not.
        """

        try:
            # Get list of ports from port range string ex: "1-53,80,443"
            ports = []
            for port_range in port_string.split(","):
                if "-" in port_range:
                    start, end = port_range.split("-")
                    ports += list(range(int(start), int(end)+1))
                else:
                    ports.append(int(port_range))

            # Remove duplicates
            ports = list(set(ports))

            # Ensure ports are in valid range
            for port in ports:
                if port < 1 or port > 65535:
                    logger.error(f"Invalid port range string: {port_string}")
                    return False, None

        except Exception as e:
            logger.error(f"Invalid port range string: {port_string}")
            return False, None

        return True, ports

        
