import typing as t

from game.converter import add_converter
from game.game import Game

add_converter()

__all__: t.Sequence[str] = ("Game",)
