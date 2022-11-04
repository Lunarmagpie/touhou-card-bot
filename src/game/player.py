import dataclasses
import hikari
import asyncio
import random
import functools
import copy
import cards
import collections


@dataclasses.dataclass
class Player:
    user: hikari.User

    # Card Related
    deck: list[int] = dataclasses.field(
        default_factory=functools.partial(copy.copy, [2, 4, 12, 13, 14, 17, 22, 25, 29, 30, 41, 58])  # type: ignore
    )
    hand: list[int] = dataclasses.field(default_factory=list)
    selected_card: int | None = None
    selected_card_event: asyncio.Event = dataclasses.field(default_factory=asyncio.Event)

    # Score Related
    seals: dict[cards.Elements, int] = dataclasses.field(
        default_factory=functools.partial(collections.defaultdict, default=0)  # type: ignore
    )

    def on_round_start(self) -> None:
        self.selected_card_event.clear()
        self.selected_card = None

        if len(self.hand) < 5:
            self.draw_card()

    def __post_init__(self) -> None:
        random.shuffle(self.deck)

        first_5 = self.deck[:5]
        self.deck[:5] = []

        self.hand.extend(first_5)

    def add_seal(self) -> None:
        """Add a seal for the player's currently selected card."""
        if not self.selected_card:
            raise ValueError("Player has no card selected.")
        card = cards.CARDS[self.selected_card]
        if card.type not in self.seals:
            self.seals[card.type] = 0
        self.seals[card.type] += 1

    def pop_from_hand(self, index: int) -> int:
        return self.hand.pop(index)

    def draw_card(self) -> None:
        if self.deck:
            self.hand.append(self.deck.pop())
