import flare
from bot.game.game import Game
import typing as t

__all__: t.Sequence[str] = ("add_converter",)

_games: dict[int, Game] = {}


class GameConverter(flare.Converter[Game]):
    async def to_str(self, obj: Game) -> str:
        _games[id(obj)] = obj
        return str(id(obj))

    async def from_str(self, obj: str) -> Game:
        id = int(obj)
        return _games[id]


def add_converter() -> None:
    flare.add_converter(Game, GameConverter)
