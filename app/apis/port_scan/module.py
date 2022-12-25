from contextlib import closing
import datetime
import socket
from apis.port_scan.model import PortScan, PortScanProtocol
from logs.logs import get_logger
import errno
import time

# Setup logger using defaults
logger = get_logger(__name__)

class PortScanModule:
    def __init__(self, scan_timeout_ms:int=500) -> None:
        self.scan_timeout_ms = scan_timeout_ms

    def get_default_timeout(self):
        return self.scan_timeout_ms

    def check_port_open_on_device(self, device_address:str, port:int, protocol:PortScanProtocol=PortScanProtocol.TCP)->bool|PortScan:
        """
        Tests if a port is open on a device.
        """
        # Result object
        result = PortScan(
            device_address          = device_address,
            port                    = port,
            protocol                = protocol,
            scan_max_duration_ms    = self.scan_timeout_ms
        )

        # Try different protocols
        # Note - Only TCP is supported at this time
        try:
            if protocol == PortScanProtocol.TCP:
                # Setup socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Set timeout and convert to seconds
                s.settimeout(self.scan_timeout_ms/1000)

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
                result.scan_duration_ms = (end_time - start_time).total_seconds()*1000

                # Log and return
                logger.debug(f"Host [{device_address}] on port [{port}] on protocol [{protocol}] is [open] after waiting [{self.scan_timeout_ms}] seconds.")
                return True, result

        except TimeoutError as e:
            # Success, but port isn't open
            logger.debug(f"Host [{device_address}] on port [{port}] on protocol [{protocol}] is [closed] after waiting [{self.scan_timeout_ms}] seconds.")

            # Set duration to timeout to keep results clean
            result.scan_duration_ms = self.scan_timeout_ms
            
            # Return
            return True, result
            
        except Exception as e:
            # Failure in general
            logger.warn(f"Host [{device_address}] on port [{port}] on protocol [{protocol}] is [unknown] after waiting [{self.scan_timeout_ms}] seconds. Error: {e}")
            return False, result