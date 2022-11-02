import dataclasses
import hikari
import asyncio


@dataclasses.dataclass
class Player:
    user: hikari.User
    selected_card: int | None = None
    selected_card_event: asyncio.Event = dataclasses.field(default_factory=asyncio.Event)

    def clear(self) -> None:
        self.selected_card_event.clear()
        self.selected_card = None
