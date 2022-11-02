import typing
import math
import enum

class Elements(enum.Enum):
    WOOD = 0
    FIRE = 1
    EARTH = 2
    METAL = 3
    WATER = 4

    def __sub__(self, o):
        out = self.value - o.value

        if out > 4:
            return out - 5

        if out < 0:
            return out + 5

        return out

class Results(enum.Enum):
    P1_WIN = enum.auto()
    P2_WIN = enum.auto()
    TIE = enum.auto()

class Card(typing.NamedTuple):
  number: int
  value: str
  type: str
  SpecialEffect = typing.NewType("SpecialEffect", int)