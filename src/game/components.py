from __future__ import annotations

import flare

import hikari
from game.game import Game
from game.player import Player
import contextlib


@flare.button()
async def card_button(ctx: flare.Context, player: Player, game: Game, number: int) -> None:
    player.selected_card_event.set()
    player.selected_card = number

    # There is an edge-case where a message is deleted right as a player chooses a card.
    # A `NotFoundError` is expected in that case.
    with contextlib.suppress(hikari.NotFoundError):
        await ctx.edit_response(
            content=f"You selected card `{number}`.", flags=hikari.MessageFlag.EPHEMERAL
        )


async def build_card_buttons(player: Player, game: Game) -> flare.Row:
    row = flare.Row()

    for i in range(5):
        row.append(card_button(player, game, i).set_label(str(i)))

    return await row  # type: ignore
