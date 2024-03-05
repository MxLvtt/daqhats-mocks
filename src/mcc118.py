"""Mocks for MCC118 boards"""

from __future__ import annotations
from dataclasses import dataclass
import math
from multiprocessing import Process, Queue
from time import sleep, time_ns

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

def time_ms() -> float:
    return time_ns() / (1000.0**2)

class mcc118:
    """MCC118 board handler"""
    def __init__(self, address: int) -> None:
        self._address = address
        self._curr_channels: list[int] = None
        self._curr_scan_rate: float = None
        self._curr_options: int = None
        self._scan_process: Process | None = None

    def _running(self) -> bool:
        return self._scan_process is not None

    def _scan_process_target(
        self,
        sample_rate_per_channel: float,
        sample_buffer: Queue,
        last_read_ms: float,
        channels: list[int]
    ) -> None:
        t_0 = last_read_ms
        s_Td_buff = 0.0
        sr_ms = sample_rate_per_channel / 1000.0
        dt_S_ms = 1.0 / sr_ms
        def C(t_ms: float) -> float:
            return math.sin(2 * math.pi * (t_ms / 800.0))
        def add_samples_to_buffer(num: int, t_read: float):
            print(f"Adding {num} samples to buffer!")
            for n in range(0, num):
                C_n = C(t_read + dt_S_ms * n - t_0)
                sample_buffer.put(C_n)
        while True:
            sleep(1.0 / 1000.0)
            num_samples_to_add = 0
            now_ms = time_ms()
            dt_r_ms = now_ms - last_read_ms
            s_T = sr_ms * dt_r_ms
            s_Ti = int(s_T)
            s_Td = s_T - s_Ti
            s_Td_buff += s_Td
            num_samples_to_add += s_Ti + int(s_Td_buff)
            add_samples_to_buffer(num_samples_to_add, last_read_ms)
            s_Td_buff -= int(s_Td_buff)
            last_read_ms = now_ms

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
        self._buffer = Queue()
        self._scan_process = Process(
            target=self._scan_process_target,
            args=(
                sample_rate_per_channel,
                self._buffer,
                time_ms(),
                self._curr_channels
            )
        )
        self._scan_process.start()

    def a_in_scan_read(self, samples_per_channel: int, timeout: float) -> Mcc118ScanResult:
        """Read a batch of samples from the current scan"""
        fix_sample_count = 10
        samples = []
        while not self._buffer.empty():
            samples.append(self._buffer.get())
        return Mcc118ScanResult(
            running=self._running(),
            hardware_overrun=False,
            buffer_overrun=False,
            triggered=self._running(),
            timeout=False,
            data=samples
        )

    def a_in_scan_cleanup(self) -> None:
        """Cleanup the scan and free the buffer"""
        return

    def a_in_scan_stop(self) -> None:
        """Stop the scan"""
        if self._scan_process is not None:
            self._scan_process.kill()
            self._scan_process = None
        self.a_in_scan_cleanup()

    def _channels_from_mask(self, channel_mask: int) -> list[int]:
        max_channel_count = 8
        channels = []
        for channel_idx in range(max_channel_count):
            channel_active = (channel_mask >> channel_idx) & 0x1
            if not channel_active:
                continue
            channels.append(channel_idx)
        return channels
