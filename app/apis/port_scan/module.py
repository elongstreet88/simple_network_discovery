import datetime
import socket
from apis.port_scan.model import PortScan, PortScanProtocol, PortScanSettings
from logs.logs import get_logger

# Setup logger using defaults
logger = get_logger(__name__)

class PortScanModule:
    def check_port_open_on_device(self, device_address:str, port:int, scan_settings:PortScanSettings)->bool|PortScan:
        """
        Tests if a port is open on a device.
        """
        # Result object
        result = PortScan(
            device_address          = device_address,
            port                    = port,
            port_scan_settings      = scan_settings
        )

        # Try different protocols
        # Note - Only TCP is supported at this time
        try:
            if scan_settings.protocol == PortScanProtocol.TCP:
                # Setup socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Set timeout and convert to seconds
                s.settimeout(scan_settings.timeout/1000)

                # Start timer
                start_time = datetime.datetime.now()

                # Try to connect
                s.connect((device_address, port))

                # Close socket
                s.close()

                # End timer
                end_time = datetime.datetime.now()

                # If we made it here, the port is considered open
                result.open = True

                # Calculate duration of port scan
                result.scan_duration = (end_time - start_time).total_seconds()*1000

                # Log and return
                logger.debug(f"Host [{device_address}] on port [{port}] with scan settings [{scan_settings}] is [open].")
                return True, result
 
        except Exception as e:
            # Success, but port isn't open or an error occurred.
            logger.debug(f"Host [{device_address}] on port [{port}] with scan settings [{scan_settings}] is [closed]. Error: {e}")

            # Set duration to timeout to keep results clean
            result.scan_duration = scan_settings.timeout
            
            # Return
            return True, result