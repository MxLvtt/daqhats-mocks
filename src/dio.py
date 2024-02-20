"""General mocks for DIO boards"""

from enum import IntEnum

class DIOConfigItem(IntEnum):
    DIRECTION = 1
    PULL_CONFIG = 2
    PULL_ENABLE = 3
    INPUT_LATCH = 4
    INT_MASK = 5
