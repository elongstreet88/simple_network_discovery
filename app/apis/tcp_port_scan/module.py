import asyncio
import datetime
from apis.tcp_port_scan.model import TCPPortScan, TCPPortScanSettings
from logs.logs import get_logger
from asyncio import Semaphore

# Setup logger using defaults
logger = get_logger(__name__)

class TCPPortScanModule:
    def __init__(self, port_scan_settings:TCPPortScanSettings=TCPPortScanSettings(), max_concurrent_connections:int=8):
        """
        Initializes the PortScanModule class.

        Args:
            max_coroutine_limit (int, optional): Maximum number of concurrent scans.
        """
        self.semaphore          = Semaphore(max_concurrent_connections)
        self.port_scan_settings = port_scan_settings

    async def check_port_open_on_device(self, device_address:str, port:int)->bool|TCPPortScan:
        """
        Checks if a port is open on a device.

        Args:
            device_address (str): IP or hostname of device being scanned
            port (int): Port being scanned
            scan_settings (PortScanSettings): Settings used for port scan.

        Returns:
            bool|PortScan: True if port is open, False if port is closed|PortScan object with details
        """

        await self.semaphore.acquire()

        # Result object
        result = TCPPortScan(
            device_address          = device_address,
            port                    = port
        )

        # Create a connection
        conn = asyncio.open_connection(device_address, port)

        try:
            # Start timer
            start_time = datetime.datetime.now()

            # Wait for connection to be made (we dont actually need the connection)
            reader, writer = await asyncio.wait_for(conn, timeout=0.5)

            # End timer
            end_time = datetime.datetime.now()

            # If we made it here, the port is considered open
            result.open = True

            # Calculate duration of port scan
            result.scan_duration = (end_time - start_time).total_seconds()*1000

            # Close connections
            writer.close()
            await writer.wait_closed()
            
            # Log and return
            logger.debug(f"Host [{device_address}] on port [{port}] with scan settings [{self.port_scan_settings}] is [open].")
            return True, result

        except asyncio.TimeoutError:
            # Success, but port isn't open
            logger.debug(f"Host [{device_address}] on port [{port}] with scan settings [{self.port_scan_settings}] is [closed].")

            # Set duration to timeout to keep results clean
            result.scan_duration = self.port_scan_settings.tcp_port_scan_timeout
            
            # Return
            return True, result

        except Exception as e:
            # Success, but port isn't open
            logger.debug(f"Host [{device_address}] on port [{port}] with scan settings [{self.port_scan_settings}] is [unknown]. Error: {e}")
            return False, None

        finally:
            self.semaphore.release()
            conn.close()
