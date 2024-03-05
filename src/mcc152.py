"""Mocks for MCC152 boards"""

from .dio import DIOConfigItem

class mcc152:
    """MCC152 board handler"""
    def __init__(self, address: int) -> None:
        self._address = address
        self._running = False
        self._last_input_read = 0

    def dio_reset(self) -> None:
        """Reset digital I/O to default settings"""
        return

    def dio_input_read_port(self) -> any:
        """Read current input port values"""
        return None

    def dio_input_read_tuple(self) -> None:
        """Read the current values of the digital input ports and return result as tuple"""
        self._last_input_read = self._last_input_read ^ 0x1
        return (self._last_input_read,) * 1

    def dio_config_write_port(self, config_item: DIOConfigItem, value: int) -> None:
        """Set digital I/O port configuration"""
        return

    def dio_int_status_read_tuple(self) -> None:
        """Read the interrupt status for the digital input ports and return result as tuple.
        
        Indicates on which channels an interrupt was detected.
        """
        return (1,) * 1
