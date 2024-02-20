"""Mocks for MCC152 boards"""

from .dio import DIOConfigItem

class mcc152:
    """MCC152 board handler"""
    def __init__(self, address: int) -> None:
        self._address = address
        self._running = False

    def dio_reset(self) -> None:
        """Reset digital I/O to default settings"""
        return

    def dio_input_read_port(self) -> any:
        """Read current input port values"""
        return None

    def dio_input_read_tuple(self) -> None:
        """Read the current values of the digital input ports and return result as tuple"""
        return (1,) * 8

    def dio_config_write_port(self, config_item: DIOConfigItem, value: int) -> None:
        """Set digital I/O port configuration"""
        return

    def dio_int_status_read_tuple(self) -> None:
        """Read the interrupt status for the digital input ports and return result as tuple"""
        return (1,) * 8

    def _channels_from_mask(self, channel_mask: int) -> list[int]:
        max_channel_count = 8
        channels = []
        for channel_idx in range(max_channel_count):
            channel_active = (channel_mask >> channel_idx) & 0x1
            if not channel_active:
                continue
            channels.append(channel_idx)
        return channels
