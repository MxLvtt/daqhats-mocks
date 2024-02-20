from dataclasses import dataclass
from enum import IntEnum

class HatError(Exception):
    """Hat specific error class"""
    pass

@dataclass
class DAQHatResult:
    """
    address (int):
        device address
    id (int):
        device product ID, identifies the type of DAQ HAT
    version (int):
        device hardware version
    product_name (str):
        device product name
    """
    address: int
    id: int
    version: int
    product_name: str

class HatIDs(IntEnum):
    """Hat board IDs"""
    ALL = 0
    MCC_118 = 1
    MCC_152 = 2

def hat_list(filter_by_id: int = HatIDs.ALL) -> list[DAQHatResult]:
    return [
        DAQHatResult(
            address=0,
            id=filter_by_id,
            version=1,
            product_name="MOCK_HAT"
        )
    ]
