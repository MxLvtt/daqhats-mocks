"""Mocks for MCC118 boards"""

from dataclasses import dataclass

@dataclass
class Mcc118ScanResult:
    """MCC118 board scan result data
    
    running (bool):
        True if the scan is running, False if it has stopped or completed.
    hardware_overrun (bool):
        True if the hardware could not acquire and unload samples fast enough
        and data was lost.
    buffer_overrun (bool):
        True if the background scan buffer was not read fast enough and data
        was lost.
    triggered (bool):
        True if the trigger conditions have been met and data acquisition
        started.
    timeout (bool):
        True if the timeout time expired before the specified number of
        samples were read.
    data (list of float):
        The data that was read from the scan buffer.
    """
    running: bool
    hardware_overrun: bool
    buffer_overrun: bool
    triggered: bool
    timeout: bool
    data: list[float]

class mcc118:
    """MCC118 board handler"""
    def __init__(self, address: int) -> None:
        self._address = address
        self._running = False
        self.a_in_scan_cleanup()

    def a_in_scan_actual_rate(self, channel_count: int, sample_rate_per_channel: float) -> float:
        """Calculate and return the actual scan rate"""
        return (sample_rate_per_channel * channel_count) / channel_count

    def a_in_scan_start(
        self,
        channel_mask: int,
        samples_per_channel: int,
        sample_rate_per_channel: float,
        options: int
    ) -> None:
        """Start a scan with the given configuration"""
        self._curr_channels = self._channels_from_mask(channel_mask)
        self._curr_scan_rate = sample_rate_per_channel
        self._curr_options = options
        self._running = True

    def a_in_scan_read(self, samples_per_channel: int, timeout: float) -> Mcc118ScanResult:
        """Read a batch of samples from the current scan"""
        fix_sample_count = 10
        samples = []
        if samples_per_channel > 0:
            samples = [1.74] * len(self._curr_channels) * samples_per_channel
        elif samples_per_channel < 0:
            samples = [1.74] * len(self._curr_channels) * fix_sample_count
        return Mcc118ScanResult(
            running=self._running,
            hardware_overrun=False,
            buffer_overrun=False,
            triggered=self._running,
            timeout=False,
            data=samples
        )

    def a_in_scan_cleanup(self) -> None:
        """Cleanup the scan and free the buffer"""
        self._curr_channels: list[int] = None
        self._curr_scan_rate: float = None
        self._curr_options: int = None

    def a_in_scan_stop(self) -> None:
        """Stop the scan"""
        self.a_in_scan_cleanup()
        self._running = False

    def _channels_from_mask(self, channel_mask: int) -> list[int]:
        max_channel_count = 8
        channels = []
        for channel_idx in range(max_channel_count):
            channel_active = (channel_mask >> channel_idx) & 0x1
            if not channel_active:
                continue
            channels.append(channel_idx)
        return channels
