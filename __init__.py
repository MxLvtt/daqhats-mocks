# pylint: disable=C0103
"""daqhats mock library for local development"""

from .config import mock_config

from .setup import run_setup

from .src.dio import DIOConfigItem
from .src.hat import HatError, HatIDs, hat_list
from .src.interrupts import (
    HatCallback, interrupt_callback_disable, interrupt_callback_enable
)

from .src.mcc118 import mcc118
from .src.mcc152 import mcc152

from .src.options import OptionFlags

run_setup()
