import enum
import typing as t

import hikari

__all__: t.Sequence[str] = ("Emoji",)


class Emoji(enum.Enum):
    # Elements
    WOOD = hikari.Emoji.parse("<:Wood:1037482562001588264>")
    FIRE = hikari.Emoji.parse("<:Fire:1037482558885212240>")
    EARTH = hikari.Emoji.parse("<:Earth:1037482557492703402>")
    METAL = hikari.Emoji.parse("<:Metal:1037482559925407775>")
    WATER = hikari.Emoji.parse("<:Water:1037482560877502564>")

    # Blank Space
    BLANK = hikari.Emoji.parse("<:__:1037952245804826765>")

    def __str__(self) -> str:
        return self.value.mention
