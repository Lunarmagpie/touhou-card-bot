from __future__ import annotations

import typing as t
import enum
import json

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
    name: str
    value: t.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    type: Elements
    special_effect: SpecialEffectT

    @t.final
    @classmethod
    def from_json(cls, index: int, d: dict[str, t.Any]) -> Card:
        return cls(
            number=index,
            name=d["name"],
            value=d["value"],
            type=Elements.__dict__[d["type"]],
            special_effect=d["special_effect"],
        )


with open("resources/cards.json") as f:
    CARDS = {
        int(index):Card.from_json(int(index), data)
        for index, data in t.cast(dict[str, t.Any], json.load(f)).items()
    }

print(CARDS)
