from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Position:
    """불변 위치 객체"""
    row: int
    col: int
    
    def __post_init__(self):
        if not (0 <= self.row < 4 and 0 <= self.col < 4):
            raise ValueError("Invalid position")
    
    def to_tuple(self) -> Tuple[int, int]:
        return (self.row, self.col)
    
    @classmethod
    def from_tuple(cls, pos_tuple: Tuple[int, int]) -> 'Position':
        return cls(pos_tuple[0], pos_tuple[1]) 