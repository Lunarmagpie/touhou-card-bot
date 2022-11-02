import enum
from bot.cards.card import Card
import typing as t

__all__: t.Sequence[str] = (
    "InteractionResults",
    "interactions",
)


class InteractionResults(enum.Enum):
    P1_WIN = enum.auto()
    P2_WIN = enum.auto()
    TIE = enum.auto()


def interactions(card_1: Card, card_2: Card) -> InteractionResults:
    if card_1.type - card_2.type == 2:
        return InteractionResults.P2_WIN

    if card_1.type - card_2.type == 3:
        return InteractionResults.P1_WIN

    if card_1.type - card_2.type in [0, 1, 4]:
        if card_1.value > card_2.value:
            return InteractionResults.P1_WIN

        if card_1.value < card_2.value:
            return InteractionResults.P2_WIN

    return InteractionResults.TIE
