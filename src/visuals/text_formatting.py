import typing as t
from game.player import Player
from cards.card import CARDS

__all__: t.Sequence[str] = ("format_names", "format_seals", "format_results")


def format_names(player_1: str, player_2: str, length: int) -> str:
    length -= len(player_1) + len(player_2)
    return f"`{player_1 + (' ' * length) + player_2}`"


def format_seals(player_1_seals: list[str], player_2_seals: list[str], length: int) -> str:
    out = ""
    offset_number = len(player_1_seals[0].split("<")) + len(player_2_seals[0].split("<"))
    for i in range(0, 3):
        if i < len(player_1_seals):
            out += player_1_seals[i]
        else:
            out += "　  " * len(player_1_seals[0].split("<"))

        out += "　  " * int(length - offset_number)

        if i < len(player_2_seals):
            out += player_2_seals[i]
        out += "\n"
    return out


def format_results(p1: Player, p2: Player, results: tuple[Player, Player]) -> str:
    out = ""
    if type(p1.selected_card) == int and type(p2.selected_card) == int:
        c1 = CARDS[p1.selected_card]
        c2 = CARDS[p2.selected_card]
        out = f"{p1.user.mention} played **{c1.name} {c1.type_icon}{c1.value}**.\n {p2.user.mention} played **{c2.name} {c2.type_icon}{c2.value}**.\n"
    if results != None:
        if c1.type != c2.type:
            out += f"The winner is {results[0].user.mention}, because {results[0].user.mention} played a card of a winning element."
        else:
            out += f"The winner is {results[0].user.mention}, because {results[0].user.mention} played a card with a higher number."
    else:
        out = "Round 1. No results yet."
    return out
