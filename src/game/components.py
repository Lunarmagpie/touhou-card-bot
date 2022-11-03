from __future__ import annotations

import flare

import hikari
from game.game import Game
from game.player import Player
import contextlib


@flare.button()
async def card_button(ctx: flare.Context, player: Player, game: Game, number: int) -> None:
    player.selected_card_event.set()
    player.selected_card = player.pop_from_hand(number)

    # If the interaction is processed after the card selection message is deleted, a
    # forbidden error would be raised.
    with contextlib.suppress(hikari.NotFoundError):
        # Remove the interaction failed response without changing anything.
        await ctx.edit_response()


async def build_card_buttons(player: Player, game: Game, card_count: int) -> flare.Row:
    row = flare.Row()

    for i in range(card_count):
        row.append(card_button(player, game, i).set_label(str(i + 1)))

    return await row  # type: ignore


@flare.button(label="Reshow Card Selection", style=hikari.ButtonStyle.SECONDARY)
async def show_card_selection(
    ctx: flare.Context, player_one: Player, player_two: Player, game: Game
) -> None:
    if ctx.user.id == player_one.user.id:
        await ctx.respond(
            component=await build_card_buttons(player_one, game, len(player_one.hand)),
            flags=hikari.MessageFlag.EPHEMERAL,
        )
    elif ctx.user.id == player_one.user.id:
        await ctx.respond(
            component=await build_card_buttons(player_two, game, len(player_two.hand)),
            flags=hikari.MessageFlag.EPHEMERAL,
        )
    else:
        await ctx.respond("You are not part of the game.", flags=hikari.MessageFlag.EPHEMERAL)
