from anyio import Semaphore
from apis.ping_scan.model import PingScan, PingScanSettings
from logs.logs import get_logger
from icmplib import async_ping

# Setup logger using defaults
logger = get_logger(__name__)

class PingScanModule:
    def __init__(self, ping_scan_settings:PingScanSettings=PingScanSettings(), max_concurrent_connections:int=8):
        """
        Initializes the PortScanModule class.

        Args:
            max_coroutine_limit (int, optional): Maximum number of concurrent scans.
        """
        self.semaphore          = Semaphore(max_concurrent_connections)
        self.ping_scan_settings = ping_scan_settings

    async def ping_device(self, device_address:str)->bool|PingScan:
        """
        Pings a device and returns the results.

        Args:
            device_address (str): IP or hostname of device being scanned
            ping_scan_settings (PingScanSettings): Settings used for ping scan.

        Returns:
            bool|PingScan: True if ping was successful, False if ping failed|PingScan object with details
        """

        # Result object
        result = PingScan(
            device_address      = device_address
        )

        # Execute ping
        ping_result = None

        # Get semaphore lock
        await self.semaphore.acquire()

        try:
            ping_result = await async_ping(
                address         = device_address,
                payload_size    = self.ping_scan_settings.ping_scan_size,
                timeout         = self.ping_scan_settings.ping_scan_timeout,
                count           = self.ping_scan_settings.ping_scan_count,
                interval        = self.ping_scan_settings.ping_scan_interval,
                privileged      = False,
            )

            # Set results
            result.online           = ping_result.is_alive
            result.average_rtt      = ping_result.avg_rtt
            result.jitter           = ping_result.jitter
            result.max_rtt          = ping_result.max_rtt
            result.min_rtt          = ping_result.min_rtt
            result.packets_sent     = ping_result.packets_sent
            result.packets_received = ping_result.packets_received
            result.packet_loss      = ping_result.packet_loss

            # Log and return
            logger.info(f"Device [{device_address}] ping online status is [{result.online}].")
            return True, result

        except Exception as e:
            logger.error(f"Error pinging device [{device_address}]. Error: [{e}].")
            return False, None

        finally:
            # Release semaphore lock
            self.semaphore.release()