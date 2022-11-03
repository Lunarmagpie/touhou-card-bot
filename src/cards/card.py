from __future__ import annotations
from tokenize import Special

import typing as t
import enum
import json

__all__: t.Sequence[str] = ("SpecialEffectT", "Elements", "Card", "CARDS")

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

icons = {
    Elements.WOOD : "<:Wood:1037482562001588264>",
    Elements.FIRE : "<:Fire:1037482558885212240>",
    Elements.EARTH : "<:Earth:1037482557492703402>",
    Elements.METAL :  "<:Metal:1037482559925407775>",
    Elements.WATER : "<:Water:1037482560877502564>"
}

special_effects = {
    0 : "This card has no special abilities.",
    1 : "After this card is played, the value of your next card played will be increased by 2.",
    4 : "After this card is played, the next winning card will award double the number of seals.",
    8 : "After this card is played, the next winning water card will award double the number of seals."
}

class Card(t.NamedTuple):
    number: int
    name: str
    img_name: str
    value: t.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    type: Elements
    special_effect: SpecialEffectT

    @t.final
    @classmethod
    def from_json(cls, index: int, d: dict[str, t.Any]) -> Card:
        return cls(
            number=index,
            name=d["name"],
            img_name=d["img_name"],
            value=d["value"],
            type=Elements.__dict__[d["type"]],
            special_effect=d["special_effect"],
        )

    @property
    def type_icon(self) -> str:
        return icons[self.type]

    @property
    def special_effect_desc(self) -> str:
        return special_effects[self.special_effect]


with open("resources/cards.json") as f:
    CARDS = {
        int(index): Card.from_json(int(index), data)
        for index, data in t.cast(dict[str, t.Any], json.load(f)).items()
    }
