
import json

from dataclasses import dataclass
from pathlib import Path

@dataclass
class BoardConfig:
    product_name: str
    board_type: int
    address: int

@dataclass
class TriggerConfig:
    duty_cycle: float
    period: float

@dataclass
class Config:
    connected_boards: list[BoardConfig]
    trigger: TriggerConfig

    def __init__(self,
                 connected_boards: list[dict],
                 trigger: dict):
        self.connected_boards = map(
            lambda board_dict: BoardConfig(**board_dict),
            connected_boards
        )
        self.trigger = TriggerConfig(**trigger)

mock_config = None

if mock_config is None:
    with Path(__file__).with_name('mockconfig.json').open('r') as _mock_config_file:
        _mock_config_dict = json.load(_mock_config_file)
        mock_config = Config(**_mock_config_dict)
