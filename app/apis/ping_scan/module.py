from apis.ping_scan.model import PingScan, PingScanSettings
from logs.logs import get_logger
from icmplib import ping

# Setup logger using defaults
logger = get_logger(__name__)

class PingScanModule:
    def ping_device(self, device_address:str, ping_scan_settings:PingScanSettings)->bool|PingScan:
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
            device_address      = device_address,
            ping_scan_settings  = ping_scan_settings,
        )

        # Execute ping
        ping_result = None
        try:
            ping_result = ping(
                address         = device_address,
                payload_size    = ping_scan_settings.size,
                timeout         = ping_scan_settings.timeout,
                count           = ping_scan_settings.count,
                interval        = ping_scan_settings.interval,
                privileged      = False,
            )
        except Exception as e:
            logger.error(f"Error pinging device [{device_address}]. Error: [{e}].")
            return False, None

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
