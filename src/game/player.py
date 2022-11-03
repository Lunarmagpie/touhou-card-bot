import dataclasses
import hikari
import asyncio
import random
import functools
import copy


@dataclasses.dataclass
class Player:
    user: hikari.User

    # Changes during gameplay
    deck: list[int] = dataclasses.field(
        default_factory=functools.partial(copy.copy, [2, 4, 12, 13, 14, 17, 22, 25, 29, 30, 41, 58])  # type: ignore
    )
    hand: list[int] = dataclasses.field(default_factory=list)
    selected_card: int | None = None
    selected_card_event: asyncio.Event = dataclasses.field(default_factory=asyncio.Event)

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

    def pop_from_hand(self, index: int) -> int:
        return self.hand.pop(index)

    def draw_card(self) -> None:
        if self.deck:
            self.hand.append(self.deck.pop())
