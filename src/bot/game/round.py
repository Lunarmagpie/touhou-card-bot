from __future__ import annotations

import flare
import typing as t

import hikari
from bot.game.game import Game


@flare.button()
async def card_button(ctx: flare.Context, game: Game, number: int) -> None:
    await ctx.respond(f"Selected card {number} on game {game}", flags=hikari.MessageFlag.EPHEMERAL)


async def build_card_buttons(game: Game) -> flare.Row:
    row = flare.Row()

    for i in range(5):
        row.append(card_button(game, i).set_label(str(i)))

    return await row
