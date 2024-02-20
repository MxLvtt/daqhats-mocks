from dataclasses import dataclass
from enum import IntEnum

from .. import mock_config

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
    results: list[DAQHatResult] = []

    for connected_board in mock_config.connected_boards:
        if filter_by_id != HatIDs.ALL and filter_by_id != connected_board.board_type:
            continue
        hat_result = DAQHatResult(
            address=connected_board.address,
            id=connected_board.board_type,
            version=1,
            product_name=connected_board.product_name
        )
        results.append(hat_result)

    print(results)

    return results
