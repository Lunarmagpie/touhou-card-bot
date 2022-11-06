# flake8: noqa

from email.mime import image
import crescent
import hikari

import utils
from cards.card import Elements, icons

plugin = utils.Plugin()


@plugin.include
@crescent.command(description="View your profile or the profile of another player.")
async def profile(ctx: utils.Context) -> None:

    embed = hikari.Embed(
            title=f"{ctx.user.username}'s Profile",
            description="?",
            color="#8e75de"
            )
    embed.add_field(
        "Current level",
        "<:xp_full_left:1038629025809174618><:xp_full_middle:1038629027252015114><:xp_full_middle:1038629027252015114><:xp_full_middle:1038629027252015114><:xp_empty_middle:1038629024026607626><:xp_empty_right:1038629024685109320>"
        "\nLevel **10** • **68/100** XP to **11**",
        inline=False,
    )
    embed.add_field(
        "Resources",
        "🪙 Coins **1,893**",
        inline=True,
    )
    embed.add_field(
        "Statistics",
        "Games played **14**"
        "\nCards discovered **12/60**",
        inline=True,
    )
    embed.add_field(
        "Favorite card",
        "Alice Margatroid",
        inline=False,
    )
    embed.set_image(
        hikari.File("resources/card_png/alice_margatroid.png")
    )

    await ctx.respond(embed=embed)
