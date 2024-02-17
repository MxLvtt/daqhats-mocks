from dataclasses import dataclass

class HatError(Exception):
    """Hat specific error class"""
    pass

@dataclass
class HatIDs:
    """Hat board IDs"""
    MCC_118 = 1
