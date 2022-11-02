import typing as t
import enum

__all__: t.Sequence[str] = ("SpecialEffectT", "Elements", "Card")

SpecialEffectT = t.NewType("SpecialEffectT", int)


class Elements(enum.Enum):
    WOOD = 0
    FIRE = 1
    EARTH = 2
    METAL = 3
    WATER = 4

    def __sub__(self, o: enum.Enum) -> int:
        out: int = self.value - o.value

        if out > 4:
            return out - 5

        if out < 0:
            return out + 5

        return out


class Card(t.NamedTuple):
    number: int
    value: str
    type: Elements
    special_effect: SpecialEffectT
