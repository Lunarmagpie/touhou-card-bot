import typing as t

__all__: t.Sequence[str] = ("format_names","format_seals")


def format_names(player_1: str, player_2: str, length: int) -> str:
    length -= (len(player_1) + len(player_2))
    return f"`{player_1 + (' ' * length) + player_2}`"

def format_seals(player_1_seals: list[str], player_2_seals: list[str], length: int) -> str:
    out = ""
    offset_number = len(player_1_seals[0].split("<")) + len(player_2_seals[0].split("<"))
    for i in range(0,3):
        if i < len(player_1_seals):
            out += player_1_seals[i]
        else:
            out += "　   " * len(player_1_seals[0].split("<"))

        out += "　   " * int(length - offset_number)

        if i < len(player_2_seals):
            out += player_2_seals[i]
        out += "\n"
    return out