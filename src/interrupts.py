"""Mocks regarding interrupt handling"""

from typing import Callable

class HatCallback:
    def __init__(self, callback_method: Callable[..., None]) -> None:
        self._callback_method = callback_method

    @property
    def callback(self) -> Callable[..., None]:
        return self._callback_method

def interrupt_callback_enable(hat_cb: HatCallback, cb_data: list) -> None:
    hat_cb.callback(cb_data)
    return

def interrupt_callback_disable() -> None:
    return
