import dataclasses
import hikari
import asyncio
import functools
import copy


@dataclasses.dataclass
class Player:
    user: hikari.User

    # Changes during gameplay
    cards: list[int] = dataclasses.field(
        default_factory=functools.partial(copy.copy, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])  # type: ignore
    )
    selected_card: int | None = None
    selected_card_event: asyncio.Event = dataclasses.field(default_factory=asyncio.Event)

    def clear(self) -> None:
        self.selected_card_event.clear()
        self.selected_card = None
