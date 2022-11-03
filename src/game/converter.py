import flare
from game.game import Game
from game.player import Player
import asyncio
import weakref
import typing as t

__all__: t.Sequence[str] = ("add_converter",)

_objects: t.MutableMapping[int, Game] = weakref.WeakValueDictionary()

# NOTE: Watch out for memory leak.
class GenericConverter(flare.Converter[t.Any]):
    async def to_str(self, obj: Game) -> str:
        _objects[id(obj)] = obj
        return str(id(obj))

    async def from_str(self, obj: str) -> Game:
        id = int(obj)
        return _objects[id]


def add_converter() -> None:
    flare.add_converter(Game, GenericConverter)
    flare.add_converter(Player, GenericConverter)
    flare.add_converter(asyncio.Event, GenericConverter)
