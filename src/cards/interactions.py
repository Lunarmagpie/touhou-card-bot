import enum
import typing as t

from cards.card import CARDS, Card

__all__: t.Sequence[str] = (
    "InteractionResults",
    "interactions",
)


class InteractionResults(enum.Enum):
    P1_WIN = enum.auto()
    P2_WIN = enum.auto()
    TIE = enum.auto()


def get_interaction_result(card_1: Card | int, card_2: Card | int) -> InteractionResults:
    if isinstance(card_1, int):
        card_1 = CARDS[card_1]
    if isinstance(card_2, int):
        card_2 = CARDS[card_2]

    return _get_interaction_result_inner(card_1, card_2)


def _get_interaction_result_inner(card_1: Card, card_2: Card) -> InteractionResults:
    if card_1.type - card_2.type in [2, 1]:
        return InteractionResults.P2_WIN

    if card_1.type - card_2.type in [3, 4]:
        return InteractionResults.P1_WIN

    if card_1.type - card_2.type in [0]:
        if card_1.value > card_2.value:
            return InteractionResults.P1_WIN

        if card_1.value < card_2.value:
            return InteractionResults.P2_WIN

    return InteractionResults.TIE
