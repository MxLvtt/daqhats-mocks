"""Mocks regarding interrupt handling"""
from __future__ import annotations

from .. import mock_config

from threading import Thread
from time import sleep
from typing import Callable

interrupt_enabled = False
int_thread: Thread | None = None

class HatCallback:
    def __init__(self, callback_method: Callable[..., None]) -> None:
        self._callback_method = callback_method

    @property
    def callback(self) -> Callable[..., None]:
        return self._callback_method

def _interrupt_thread(hat_cb: HatCallback, cb_data: list) -> None:
    high_duration = mock_config.trigger.period * mock_config.trigger.duty_cycle
    low_duration = mock_config.trigger.period - high_duration
    is_high_phase = False
    while interrupt_enabled:
        if not is_high_phase:
            sleep(low_duration)
        else:
            sleep(high_duration)
        hat_cb.callback(cb_data)
        is_high_phase = not is_high_phase

def interrupt_callback_enable(hat_cb: HatCallback, cb_data: list) -> None:
    """Enable global interrupt callback"""
    global int_thread, interrupt_enabled
    interrupt_enabled = True
    int_thread = Thread(target=_interrupt_thread, args=(hat_cb, cb_data))
    int_thread.start()

def interrupt_callback_disable() -> None:
    """Disable global interrupt callback"""
    global int_thread, interrupt_enabled
    interrupt_enabled = False
    if int_thread is None:
        return
    int_thread.join(5)
