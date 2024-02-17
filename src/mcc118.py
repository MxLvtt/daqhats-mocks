"""Mocks for MCC118 boards"""

from .options import OptionFlags

class mcc118:
    """MCC118 board handler"""
    def __init__(self, address: int) -> None:
        self._address = address

    def a_in_scan_actual_rate(self, num_channels: int, scan_rate: float) -> float:
        """Calculate and return the actual scan rate"""
        raise NotImplementedError()

    def a_in_scan_start(self, channel_mask: str, a: int, scan_rate: float, options: OptionFlags) -> None:
        """Start a scan with the given configuration"""
        raise NotImplementedError()

    def a_in_scan_cleanup(self) -> None:
        """Cleanup the scan and free the buffer"""
        raise NotImplementedError()

    def a_in_scan_stop(self) -> None:
        """Stop the scan"""
        raise NotImplementedError()

    def a_in_scan_read(self, a: int, b: int) -> None:
        """Read a batch of samples from the current scan"""
        raise NotImplementedError()
