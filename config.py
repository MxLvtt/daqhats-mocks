
import json

from dataclasses import dataclass
from pathlib import Path

@dataclass
class BoardConfig:
    product_name: str
    board_type: int
    address: int

@dataclass
class Config:
    connected_boards: list[BoardConfig]

    def __init__(self, connected_boards: list[dict]):
        self.connected_boards = map(
            lambda board_dict: BoardConfig(**board_dict),
            connected_boards
        )

with Path(__file__).with_name('mockconfig.json').open('r') as _mock_config_file:
    _mock_config_dict = json.load(_mock_config_file)
    mock_config = Config(**_mock_config_dict)
